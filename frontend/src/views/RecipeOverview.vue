<template>
  <PageHeader />

  <section class="c-recipe-image o-section">
    <div class="c-recipe-image__image-container">
      <img
        class="c-recipe-image__image"
        :src="recipe.img" :alt = "require('@/assets/ImageNotFound.png')"
      >
    </div>
  </section>
  
  <section class="c-recipe o-section">
    <div class="c-recipe__container o-container">
      <div class="c-recipe__info-container">   
        <div class="c-recipe__info-left">
          <h1 class="c-recipe__heading">
            {{ recipe.name }}
          </h1>

          <p class="c-recipe__description">
            {{ recipe.decription }}
          </p>
        </div> 

        <div class="c-recipe__info-right">
          <div class="c-recipe__meta-container">
            <p class="c-recipe__meta">
              Prep: {{ recipe.prepTime }}
            </p>

            <p class="c-recipe__meta">
              Cook: {{ recipe.cookTime }}
            </p>
            <p class="c-recipe__meta__server">
              Serving Size: {{ recipe.servingSize }}
            </p>
          </div>
        </div>
        <div class="c-recipe__info-bottom">
          <div
            class="c-recipe__bookmark-button-container"
            @click="toggleFavourite"
          >
            <BookmarkSVG
              :class="`c-recipe__bookmark-icon js-bookmark-icon ${recipe.isFavourite ? 'c-recipe__bookmark-icon--favourite' : ''}`"
            />

            <p class="c-recipe__bookmark-title">
              Bookmark Recipe
            </p>
          </div>
          <div class="c-recipe__info-bottom">
            <div v-if="recipe.Voices" class="c-recipe__dropdown-container">
              <select  v-model="selectedVoice">
                <option value="" disabled selected>Choose your voice</option>
                <option v-for="option in recipe.Voices" :key="option" :value="option">{{  option.replace('_', ' ') }}</option>
              </select>
            </div>
            <a
                v-if="recipe.isSmart"
                class="c-recipe__link"
                :href="GetURL()"
              >start recipe</a>
              <a
                v-else
                class="c-recipe__link"
                :href="`/recipe/${ route.params.id }/false`" 
              >start recipe</a>
          </div>
        </div>
      </div>

      <RecipeSwitcher 
        :ingredients="recipe.ingredients"
        :steps="recipe.steps" 
      />
    </div> 
  </section>
</template>

<script setup>
import PageHeader from '@/components/PageHeader.vue'
import RecipeSwitcher from '@/components/RecipeSwitcher.vue'
import BookmarkSVG from '@/assets/bookmark-svg.vue'
import { useStore } from 'vuex'


import { onMounted, reactive, onBeforeUnmount,ref  } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const route = useRoute()
const store = useStore()
const socket = new WebSocket(store.state.websocketUrl)
const selectedVoice = ref('')

var recipe = reactive({
    name: 'ERROR NAME NOT FOUND',
    decription: 'ERROR DESCRIPTION NOT FOUND',
    img:  require('@/assets/ImageNotFound.png'),
    steps: [
        'Loading recipe...'
    ],
    isFavourite : false,
    ingredients: [
        'NO INGREDIENT FOUND'
    ],
    isSmart: false
})

onMounted(() => {
    getRecipeInfo()
})

function GetURL() {
    const temp = `/recipe/${route.params.id}/${selectedVoice.value ? selectedVoice.value : "false"}`
    return temp
}


function getRecipeInfo()
{
    socket.addEventListener('open', (event) => {
        socket.send(`{"command": { "keyword": "get","recipe_id": ${route.params.id} }}`)

    })
    socket.addEventListener('message', (event) => {
        const RecipeJsonMessage = JSON.parse(event.data)
        parseRecipeFromJson(RecipeJsonMessage)
    })

}


function formatIngredients(RecipeJsonMessage)
{
    const ingredients = RecipeJsonMessage['ingredients']
  
    //Get and format all the ingredients 
    var ingredientsList = []
    for(const key in ingredients){
        var ingredientFormatted = ingredients[key]['amount']
        ingredientFormatted = ingredientFormatted ? ingredientFormatted : ''
        if (ingredients[key]['unit'] !== 'unit' && ingredients[key]['unit'] != null) {
            ingredientFormatted += ' ' + ingredients[key]['unit']
        }
        ingredientFormatted += ' ' + ingredients[key]['item']
        ingredientsList.push(ingredientFormatted)
    }
    return ingredientsList
}


function parseRecipeFromJson(RecipeJsonMessage)
{
    recipe.name = RecipeJsonMessage.name
    recipe.decription = RecipeJsonMessage.description
    recipe.img = RecipeJsonMessage.image
    recipe.prepTime = formatTime(RecipeJsonMessage.prepTime)
    recipe.cookTime = formatTime(RecipeJsonMessage.cookTime)
    recipe.ingredients = formatIngredients(RecipeJsonMessage)
    recipe.isFavourite = RecipeJsonMessage.isFavourite
    recipe.steps = RecipeJsonMessage['commands']
    recipe.isSmart = RecipeJsonMessage.isSmart
    recipe.servingSize = RecipeJsonMessage.servingSize
    recipe.Voices = RecipeJsonMessage['Voices']
}

const formatTime = (Time) => {
    const hours = Math.floor(Time / 60);
    const remainingMinutes = Time % 60;
    if (hours === 0) {
        return `${remainingMinutes} minute${remainingMinutes !== 1 ? 's' : ''}`;
    } else if (remainingMinutes === 0) {
        return `${hours} hour${hours !== 1 ? 's' : ''}`;
    } else {
        return `${hours} hour${hours !== 1 ? 's' : ''} ${remainingMinutes} minute${remainingMinutes !== 1 ? 's' : ''}`;
    }
}

const toggleFavourite = ($event) => {
  console.log(selectedVoice)
    const bookmarkIcon = $event.target.parentElement
    
    if (bookmarkIcon.classList.contains('favourite')) {
        bookmarkIcon.classList.remove('favourite')
    } else {
        bookmarkIcon.classList.add('favourite')
    }
    
    recipe.isFavourite = !recipe.isFavourite
    const socket = new WebSocket(store.state.websocketUrl)
    socket.addEventListener('open', (event) => {
        socket.send('{"command": {"keyword": "favourite", "type": '+recipe.isFavourite+' ,"recipe_id": '+ route.params.id +  '}}')
    })
}

onBeforeUnmount(() => {
    socket.close()
})

</script>

<style scoped lang="scss">
.c-recipe {
  &__info-container {
    @include grid;
  }

  &__info-left {
    grid-column:1/9;

    @include media("<=tablet") {
      grid-column: 1/-1;
    }
  }

  &__heading {
    @include ts-heading-1;
    color: var(--dark-green);
    grid-column:1/7;
  }

  &__description {
    @include ts-heading-3;
    color: var(--dark-green);
    margin-top:var(--space-s);
  }

  &__info-right {
    grid-column: 9/-1;

    @include media("<=tablet") {
      grid-column: 1/-1;
    }
  }

  &__meta-container {
    background: var(--dark-green);
    border-radius: 10px;
    padding: var(--space-m);
    box-sizing: border-box;

    @include media("<=tablet") {
      padding: var(--space-xs);
      display:flex;
      flex-direction: row;
      align-items: center;
    }
  }

  &__meta {
    @include ts-heading-4;
    color: var(--white);
    display: flex;
    align-items: center;

      &__server{
        @include ts-heading-4;
        color: var(--white);
        display: flex;
        align-items: center;

        &::before{
          content:'';
          mask:url('@/assets/people-icon.png');
          background: var(--white);
          display:inline-block;
          height:28px;
          width:28px;
          mask-size: cover;
          margin-right: var(--space-xs);
        }
        @include media("<=tablet") {
          width:50%;
        }
      }

    &::before {
      content:'';
      mask:url('@/assets/clock.svg');
      background: var(--white);
      display:inline-block;
      height:28px;
      width:28px;
      mask-size: cover;
      margin-right: var(--space-xs);
    }

    @include media("<=tablet") {
      width:50%;
    }
  }

  &__meta + &__meta {
    margin-top: var(--space-xs);

    @include media("<=tablet") {
      margin-top:0;
    }
  }
  &__meta + &__meta__server {
    margin-top: var(--space-xs);

    @include media("<=tablet") {
      margin-top:0;
    }
  }

  &__info-bottom {
    grid-column: 1/-1;
    display: flex;
    justify-content: space-between;
    gap:var(--space-xxs);

    @include media("<=tablet") {
      flex-direction: column;
    }
  }

  &__bookmark-button-container {
    @include ts-heading-3;
    color:var(--dark-green);
    background: var(--white);
    display: flex;
    align-items: center;
    padding: var(--space-xxs);
    border-radius: 10px;
    border: 2px solid var(--dark-green);

    &:hover,
    &:focus {
      background-color:var(--dark-green);
      color:var(--white);
    }

    @include media("<=tablet") {
      justify-content: center;
    }
  }

  &__bookmark-icon {
    color: var(--white);
    margin-right: var(--space-xxs);

    &--favourite {
      color: var(--dark-green);
      stroke: solid 1px var(--white);
    }
  }

  &__link {
    @include ts-heading-3;
    border-radius: 10px;
    border: 2px solid var(--dark-green);
    background-color: var(--white);
    color: var(--dark-green);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-xxs);

    &:hover,
    &:focus {
      background-color: var(--dark-green);
      color: var(--white);
    }
  }
  &__info-bottom {
    grid-column: 1/-1;
    display: flex;
    justify-content: space-between;
    gap: var(--space-xxs);

    @include media("<=tablet") {
      flex-direction: column;
    }
  }
  &__dropdown-container {
    select {
      background-color: var(--white);
      border: 2px solid var(--dark-green);
      border-radius: 20px;
      padding: var(--space-xxs);
      color: var(--dark-green);
      font-size: 16px;

      &:hover,
      &:focus {
        background-color: var(--dark-green);
        color: var(--white);
      }
      @include media("<=tablet") {
        width:100%;

      }
    }
  }
}
.c-recipe-image {
  &__image-container {
    position:relative;
    height:50vh;
  }

  &__image {
    height:100%;
    width:100%;
    aspect-ratio:16/9;
    position:absolute;
    object-fit: cover;
    top:0;
    left:0;
  }
}
</style>