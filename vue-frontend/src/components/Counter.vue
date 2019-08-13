<template>
  <div>
    <p>I'm a Counter!</p>
    <div>
      <button v-on:click="increase()">Add 1</button>
      <button v-on:click="decrease()">Minus 1</button>
      <p>The button above has been clicked {{ counter }} times.</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    counter: Number
  },
  // data() {
  //   return {
  //     counter: 0
  //   };
  // },
  methods: {
    increase: function() {
      this.counter += 1;
    },
    decrease: function() {
      this.counter -= 1;
    }
  }
};
</script>

<style>
</style>

