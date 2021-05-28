<template>
  <v-container>
    <v-row class="text-center mt-4">
      <v-col> <p class="font-weight-bold title mb-10">현재 온도</p></v-col>
    </v-row>
    <v-row class="text-center">
      <v-col>
        <v-icon v-if="tempCheck" size="80" color="blue darken-1">
          mdi-emoticon
        </v-icon>
        <v-icon v-else size="80" color="red darken-1">
          mdi-emoticon-sad
        </v-icon>
      </v-col>
    </v-row>
    <v-row class="text-center mt-3">
      <v-col>
        <p class="text-h2 font-weight-bold mb-0">{{ temp }}°C</p></v-col
      >
    </v-row>
    <v-row class="text-center mb-5">
      <v-col>
        <v-btn icon @click="update"><v-icon>mdi-refresh</v-icon></v-btn></v-col
      >
    </v-row>
    <v-row class="text-center mt-3">
      <v-col cols="5" class="mt-2 ml-2"> 현재 설정 범위 : </v-col>
      <v-col class="mt-2">{{ range.lower }}°C ~ {{ range.upper }}°C</v-col>
      <v-col>
        <v-btn
          depressed
          @click="
            () => {
              dialog = true;
              range = Object.assign({}, changedRange);
            }
          "
          >수정
        </v-btn>
      </v-col>
    </v-row>
    <v-dialog
      v-if="dialog"
      v-model="dialog"
      persistent
      max-width="500"
      max-height="700"
    >
      <v-card :loading="!!isLoading" align="center">
        <v-container>
          <v-text-field
            type="number"
            v-model="changedRange.lower"
            label="하한온도"
            :error-messages="errormsg"
            required
          ></v-text-field>
          <v-text-field
            type="number"
            v-model="changedRange.upper"
            label="상한온도"
            :error-messages="errormsg"
            required
          ></v-text-field>
          <v-btn depressed class="mr-3" @click="close">수정</v-btn>
          <v-btn depressed @click="dialog = false">닫기</v-btn>
        </v-container>
      </v-card>
    </v-dialog>
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
    temp: 0,
    range: {
      upper: 0,
      lower: 0,
    },
    changedRange: {
      upper: 0,
      lower: 0,
    },
    dialog: false,
    errormsg: "",
    isLoading: false,
    snackbar: {
      show: false,
      timeout: 2000,
      text: "",
    },
  }),
  async created() {
    // 현재 온도 값, 설정 범위 값 받아오기
    await this.update();
    // 소켓처리 하면 더 좋을텐데..
  },
  computed: {
    tempCheck() {
      if (this.temp >= this.lower && this.temp <= this.upper) return true;
      else return false;
    },
  },
  methods: {
    async update() {
      try {
        const res = await axios.get("/temp");
        this.temp = res.data["temp_c"];
        const res2 = await axios.get("/temp/range");
        this.range = res2.data;
      } catch (err) {
        this.showSnackbar("error", err.message);
      }
    },
    async close() {
      if (
        this.lowerChange === "" ||
        this.upperChange === "" ||
        this.lowerChange * 1 > this.upperChange * 1
      ) {
        this.errormsg = "온도 범위를 정확히 입력해주세요.";
        return;
      }
      this.isLoading = true;
      this.range.lower = this.lowerChange;
      this.range.upper = this.upperChange;
      this.errormsg = "";
      // 서버로 범위 수정 API 보내기.
      await axios.patch("/temp/range", this.range);
      this.update();
      this.isLoading = false;
      this.dialog = false;
      this.showSnackbar("success", "범위 업데이트에 성공했습니다.");
    },
  },
};
</script>
