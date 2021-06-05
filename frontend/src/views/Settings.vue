<template>
  <v-container class="ma-5 pa-5">
    <v-row>
      <v-text-field v-model="token"></v-text-field>
      <v-btn @click="tokenChange">토큰값 재설정</v-btn>
    </v-row>
    <v-row>
      <v-text-field v-model="serverIP"></v-text-field>
      <v-btn @click="IPChange">아이피 재설정</v-btn>
    </v-row>
    <v-snackbar
      v-model="snackbar.show"
      :timeout="snackbar.timeout"
      :color="snackbar.color"
    >
      {{ snackbar.text }}

      <template v-slot:action="{ attrs }">
        <v-btn color="white" icon v-bind="attrs" @click="snackbar.show = false">
          <v-icon>mdi-close </v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    token: "",
    serverIP: "",
    snackbar: {
      show: false,
      timeout: 2000,
      text: "",
    },
  }),
  methods: {
    async tokenChange() {
      try {
        await axios.put(`/setting/token`, this.token);
        this.showSnackbar("success", "토큰 수정 성공!");
      } catch (err) {
        this.showSnackbar("error", err.message);
      }
    },
    async IPChange() {
      try {
        axios.defaults.baseURL = this.serverIP + "/api";
      } catch (err) {
        this.showSnackbar("error", err.message);
      }
    },
    showSnackbar(color, text) {
      this.snackbar.show = true;
      this.snackbar.color = color;
      this.snackbar.text = text;
    },
  },
};
</script>
