<template>
  <!-- PART 4: Add your code here -->
  <div>
    {{id}}
    {{name}}
    <Counter :counter="episodes_seen" />
  </div>
</template>

<script>
// PART 4: Add your code here
import Counter from "./Counter.vue";
export default {
  components: {
    Counter
  },
  props: {
    id: Number,
    name: String,
    episodes_seen: Number
  }
};
</script>

<style>
</style>
