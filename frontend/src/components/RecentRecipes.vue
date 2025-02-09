<template>
  <section class="c-recent-recipes o-section">
    <div class="c-recent-recipes__container o-container">
      <div class="c-recent-recipes__text-container">
        <h1 class="c-recent-recipes__heading">
          <a
            class="c-recent-recipes__heading-link"
            href="/search/Smart"
          >
            Smart Recipes
            <span class="c-recent-recipes__heading-icon">></span>
          </a>
        </h1>
      </div>

      <div
        v-if="recipesLoaded"
        class="c-recent-recipes__recipes"
      >
        <RecipeCard
          v-for="recipe in recipes"
          :id="recipe.id"
          :key="recipe.id"
          :image="recipe.image"
          :recipe-name="recipe.name"
          :info="recipe.info"
          :size="'horizontal'"
          :isSmart ="true"
          :is-favourite="recipe.isFavourite"
          :time = "recipe.time"
          @favouriteChange="handleFavouriteChange"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue'
import RecipeCard from './RecipeCard.vue'
import { useStore } from 'vuex'


const recipesLoaded = ref(false)
const recipes = ref([])
const store = useStore()

const emits = defineEmits()
const socket = new WebSocket(store.state.websocketUrl)
onMounted(async () => {

    socket.addEventListener('open', (event) => {
        socket.send('{"command": {"keyword": "get","recipe_id": -2}}')
    })

    socket.addEventListener('message', (event) => {
        const arrayRecipe = JSON.parse(event.data)
        recipes.value = arrayRecipe.map(recipe => ({ name: recipe.name, image: recipe.image, info: recipe.description , id:recipe.id, isFavourite:recipe.isFavourite, time: formatTime(recipe.prepTime , recipe.cookTime)}))
        recipesLoaded.value = true
    })
})
const handleFavouriteChange = () => {
    emits('favouriteChange')
}

onBeforeUnmount(() => {
    socket.close()
})
const formatTime = (preTime, cookTime) => {
    const totalMinutes = preTime + cookTime;
    const hours = Math.floor(totalMinutes / 60);
    const remainingMinutes = totalMinutes % 60;
    if (hours === 0) {
        return `${remainingMinutes} min${remainingMinutes !== 1 ? 's' : ''}`;
    } else if (remainingMinutes === 0) {
        return `${hours} hr${hours !== 1 ? 's' : ''}`;
    } else {
        return `${hours} hr${hours !== 1 ? 's' : ''} ${remainingMinutes} mini${remainingMinutes !== 1 ? 's' : ''}`;
    }
}

</script>

<style scoped lang="scss">
.c-recent-recipes {
  $c : &;

  &__text-container {
    display:grid;
    grid-template-columns: repeat(12, 1fr);
    grid-gap: 2rem;
  }

  &__heading {
    @include ts-heading-2;
    color: var(--dark-green);
    grid-column:1/7;
    margin-bottom: var(--space-s);
    width:fit-content;

    &:hover,
    &:focus {
      #{$c}__heading-icon {
        transform: translateX(10px);
      }
    }

    @include media("<=tablet") {
      grid-column: 1/-1;
    }
  }

  &__heading-icon {
    margin-left:8px;
    display:inline-block;
    transition: transform 0.3s;
  }

  &__recipes {
    display:grid;
    grid-template-columns: repeat(2,1fr);
    grid-gap: 2rem;

    @include media("<=tablet") {
      grid-template-columns: repeat(1,1fr);
    }
  }
}
</style>