<template>
  <section class="c-recipe-switcher o-section">
    <div class="c-recipe-swtcher__container">
      <div class="c-recipe-switcher__button-container">
        <button
          class="c-recipe-switcher__button c-recipe-switcher__button--ingredients js-ingredient-button is-toggled"
          @click="toggle('ingredient')"
        >
          Ingredients
        </button>

        <button
          class="c-recipe-switcher__button c-recipe-switcher__button--recipe js-recipe-button"
          @click="toggle('recipe')"
        >
          Recipe
        </button>
      </div> 

      <ul class="c-recipe-switcher__ingredient-container o-container js-ingredient-view is-toggled">
        <li 
          v-for="ingredient in ingredients"
          :key="ingredient"
          class="c-recipe-switcher__ingredient"
        >
          {{ ingredient }}
        </li>
      </ul> 

      <ul class="c-recipe-switcher__recipe-container js-recipe-view o-container">
        <li
          v-for="(step, index) in steps"
          :key="step"
          class="c-recipe-switcher__recipe-step"
        >
          <span>{{ index + 1 }}. </span>
          <span>{{ step }}</span>
        </li>
      </ul> 
    </div>
  </section>
</template>

<script setup>
//import { Console } from 'console';

defineProps({
    ingredients: {type : Array[String], default: 'test ingredient'},
    steps: {type : Array[String], default: 'test step'}
})

function toggle(buttonName) {
    const recipeButton = document.getElementsByClassName('js-recipe-button')[0]
    const ingredientButton = document.getElementsByClassName('js-ingredient-button')[0]

    const recipeView = document.getElementsByClassName('js-recipe-view')[0]
    const ingredientView = document.getElementsByClassName('js-ingredient-view')[0]

    if(buttonName == 'recipe' && !recipeButton.classList.contains('is-toggled')) {
        recipeButton.classList.add('is-toggled')
        ingredientButton.classList.remove('is-toggled')

        ingredientView.classList.remove('is-toggled')
        recipeView.classList.add('is-toggled')
    }
    else if(buttonName == 'ingredient' && !ingredientButton.classList.contains('is-toggled')){
        recipeButton.classList.remove('is-toggled')
        ingredientButton.classList.add('is-toggled')

        recipeView.classList.remove('is-toggled')
        ingredientView.classList.add('is-toggled')
    }
}
</script>

<style scoped lang="scss">
.c-recipe-switcher {
  $c : &;

  background-color: var(--white);
  border-radius: 30px;

  &__button-container {
    display:flex;
  }

  &__button {
    @include ts-heading-2;
    background-color: var(--dark-green);;
    color: var(--white);
    padding:var(--space-l);
    width: 50%;

    &--ingredients {
      border-radius: 30px 0px 0px 0px;
    }

    &--recipe {
      border-radius: 0px 30px 0px 0px;
    }
    &.is-toggled {
      color:var(--dark-green);;
      background-color: var(--white);
    }

    @include media("<=tablet") {
      @include ts-heading-3;
      padding: var(--space-s);
    }
  }

  &__ingredient-container,
  &__recipe-container {
    @include ts-heading-3;
    color: var(--dark-green);
    display: none;
    flex-direction: column;
    gap: 32px;
    min-height: 50vh;
    max-height: 100vh;
    overflow-y: scroll;
    padding-top: var(--space-xl);
    padding-bottom: var(--space-xl);

    &.is-toggled {
      display:flex;
    }

    @include media("<=tablet") {
      @include ts-heading-4;
      padding-top: var(--space-m);
      padding-bottom: var(--space-m);
    }
  }

  &__ingredient {
    background: rgba(65, 145, 112, 0.20);
    padding: var(--space-s);
    border-radius: 10px;

    @include media("<=tablet") {
      padding:var(--space-xs);
    }
  }

  &__recipe-step {
    @include ts-heading-3;
    color: var(--dark-green);;

    & > span {
      margin-right: var(--space-xxs);
    }

    @include media("<=tablet") {
      @include ts-heading-4;
    }
  }
}
</style>