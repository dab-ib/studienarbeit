<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn to="/" text>Overview</v-btn>
      <v-btn to="/recorded" text>Recorded</v-btn>
      <v-spacer></v-spacer>
      <v-btn to="/settings" text><v-icon>mdi-cog</v-icon></v-btn>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'App',

  components: {},

  data() {
    return {
      // Hier können Sie Ihre Daten definieren
    };
  },
});
</script>

<style>
/* Hier können Sie Ihren Stil definieren */
</style>
