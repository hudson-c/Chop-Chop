<template>
  <PageHeader 
    :search="true"
  />

  <CardListing />
</template>

<script setup>
import PageHeader from '@/components/PageHeader.vue'
import CardListing from '@/components/CardListing.vue'
</script>