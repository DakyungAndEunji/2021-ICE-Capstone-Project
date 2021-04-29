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
      <v-col class="mt-2">{{ lower }}°C ~ {{ upper }}°C</v-col>
      <v-col>
        <v-btn
          depressed
          @click="
            () => {
              dialog = true;
              lowerChange = lower;
              upperChange = upper;
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
            v-model="lowerChange"
            label="하한온도"
            :error-messages="errormsg"
            required
          ></v-text-field>
          <v-text-field
            type="number"
            v-model="upperChange"
            label="상한온도"
            :error-messages="errormsg"
            required
          ></v-text-field>
          <v-btn depressed class="mr-3" @click="close">수정</v-btn>
          <v-btn depressed @click="dialog = false">닫기</v-btn>
        </v-container>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
//import axios from "axios";

export default {
  data: () => ({
    temp: 17,
    upper: 23,
    lower: 10,
    upperChange: 0,
    lowerChange: 0,
    dialog: false,
    errormsg: "",
    isLoading: false,
  }),
  async mounted() {
    // 현재 온도 값, 설정 범위 값 받아오기
    this.update();
    // 소켓처리 하면 더 좋을텐데..
  },
  computed: {
    tempCheck() {
      if (this.temp >= this.lower && this.temp <= this.upper) return true;
      else return false;
    },
  },
  methods: {
    update() {},
    close() {
      if (
        this.lowerChange === "" ||
        this.upperChange === "" ||
        this.lowerChange * 1 > this.upperChange * 1
      ) {
        this.errormsg = "온도 범위를 정확히 입력해주세요.";
        return;
      }
      this.isLoading = true;
      this.lower = this.lowerChange;
      this.upper = this.upperChange;
      this.errormsg = "";
      this.update();
      // 서버로 범위 수정 API 보내기.
      this.isLoading = false;
      this.dialog = false;
    },
  },
};
</script>
