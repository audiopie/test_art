<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      msg: [],
    };
  },
  methods: {
  getMessage() {
    const path = 'http://127.0.0.1:5000/currencies/api/v1.0/';
    axios.get(path)
      .then((res) => {
        this.msg = res.data;
      })
      .catch((error) => {
        console.error(error);
      });
  },
  },
  created() {
    this.getMessage();
  },
};
</script>


<template>
  <div>
    <select v-model="selected">
      <option v-for="item in msg" v-bind:value="item">
        {{item.code}}
      </option>
    </select>

  </div>
</template>




