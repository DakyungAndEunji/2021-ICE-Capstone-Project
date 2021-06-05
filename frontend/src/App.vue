<template>
  <v-app>
    <v-main>
      <router-view :key="$route.fullPath"></router-view>
    </v-main>
    <v-footer app fixed padless>
      <v-bottom-navigation
        :value="this.$route.name"
        color="teal"
        grow
        class="pt-2"
      >
        <v-btn
          color="white"
          value="Temperature"
          @click="moveToPage('Temperature')"
        >
          온도
          <v-icon>mdi-thermometer</v-icon>
        </v-btn>

        <v-btn
          color="white"
          value="ProductList"
          @click="moveToPage('ProductList')"
        >
          재고관리
          <v-icon>mdi-database</v-icon>
        </v-btn>

        <v-btn
          color="white"
          value="Statistics"
          @click="moveToPage('Statistics')"
        >
          통계
          <v-icon>mdi-chart-bar</v-icon>
        </v-btn>
        <v-btn color="white" value="Settings" @click="moveToPage('Settings')">
          설정
          <v-icon>mdi-cog</v-icon>
        </v-btn>
      </v-bottom-navigation>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data: () => ({}),
  methods: {
    moveToPage(next) {
      if (this.$route.name != next) {
        this.$router.push({ name: next });
      }
    },
  },
};
</script>
