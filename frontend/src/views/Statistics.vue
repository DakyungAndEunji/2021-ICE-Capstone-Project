<template>
  <v-container class="pa-0">
    <v-tabs center-active background-color="indigo" dark v-model="tab">
      <v-tab>
        매출 현황
      </v-tab>
      <v-tab>
        시간대별 매출
      </v-tab>
      <v-tab>
        메뉴별 매출
      </v-tab>
      <v-tab-item>
        <v-row class="my-0 mx-2">
          <v-col>
            <v-menu
              ref="menu"
              v-model="menu"
              :close-on-content-click="false"
              :return-value.sync="date"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="date"
                  label="판매일자"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                :max="currentDate"
                v-model="date"
                no-title
                scrollable
              >
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="menu = false">
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="
                    () => {
                      $refs.menu.save(date);
                      this.updateData();
                    }
                  "
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              outlined
              dense
              hide-details
              clearable
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-data-table
              :loading="!!isLoading"
              loading-text="Loading... Please wait"
              v-model="selected"
              :headers="headers"
              :items="data"
              :sort-by="'order_time'"
              :sort-desc="false"
              :search="search"
              multi-sort
              item-key="order_time"
              class="elevation-1"
            >
              <template v-slot:[`item.actions`]="{ item }">
                <v-icon
                  small
                  class="mr-2"
                  @click="openProductUpdateDialog(item)"
                >
                  mdi-pencil
                </v-icon>
                <v-icon small @click="deleteItem(item)">
                  mdi-delete
                </v-icon>
              </template>
              <template v-slot:no-data>
                <v-btn color="primary" @click="initialize">
                  Reset
                </v-btn>
              </template>
            </v-data-table>
          </v-col>
        </v-row>
      </v-tab-item>
      <v-tab-item>
        This is tab 2 Page
      </v-tab-item>
      <v-tab-item>
        This is tab3 Page
      </v-tab-item>
    </v-tabs>
  </v-container>
</template>

<script>
import moment from "moment";
//import axios from "axios";

export default {
  data() {
    return {
      tab: null,
      errorMsg: "",
      date: moment().format("YYYY-MM-DD"),
      currentDate: moment().format("YYYY-MM-DD"),
      menu: false,
      totalSales: null,
      totalIncome: null,
      isLoading: false,
      data: [],
      selected: [],
      search: "",
      headers: [
        { text: "유형", align: "start", value: "order_type" },
        {
          text: "시간",
          value: "order_time",
        },
        { text: "상품명", value: "product_name" },
        { text: "수량", value: "order_number" },
      ],
    };
  },
  async created() {
    await this.updateData();
  },
  methods: {
    async updateData() {
      //서버에서 data에 해당하는 날짜의 매출목록, 총매출액, 순이익을 불러온다.
      this.totalSales = 1240000;
      this.totalIncome = 570000;
      this.data = [
        {
          order_type: 0,
          order_time: "2021/04/10 08:10",
          product_name: "사랑에 빠진 딸기",
          order_number: 5,
        },
        {
          order_type: 0,
          order_time: "2021/04/10 08:13",
          product_name: "레인보우 샤베트",
          order_number: 3,
        },
        {
          order_type: 1,
          order_time: "2021/04/10 17:28",
          product_name: "레인보우 샤베트",
          order_number: 1,
        },
        {
          order_type: 1,
          order_time: "2021/04/15 22:35",
          product_name: "사랑에 빠진 딸기",
          order_number: 2,
        },
        {
          order_type: 0,
          order_time: "2021/04/22 09:27",
          product_name: "아몬드 봉봉봉",
          order_number: 2,
        },
      ];
      this.data.forEach((val, idx) => {
        this.data[idx].order_time = moment(val.order_time).format(
          "YYYY/MM/DD HH:mm"
        );
        this.data[idx].order_type = val.order_type === 0 ? "출고" : "입고";
      });
    },
  },
};
</script>
