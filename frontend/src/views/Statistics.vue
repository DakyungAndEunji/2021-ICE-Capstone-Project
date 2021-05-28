<template>
  <v-container class="pa-0">
    <v-tabs center-active background-color="teal" dark v-model="tab">
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
        <v-row class="mb-n2 mt-0 mx-2">
          <v-col>
            <v-menu
              ref="menu"
              v-model="tab1.menu"
              :close-on-content-click="false"
              :return-value.sync="date"
              transition="scale-transition"
              offset-y
              :max-width="290"
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
                <v-btn text color="primary" @click="tab1.menu = false">
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
          </v-col>
          <v-col v-if="$vuetify.breakpoint.smAndUp">
            <v-text-field
              :max-width="290"
              v-model="tab1.search"
              append-icon="mdi-magnify"
              label="Search"
              outlined
              dense
              hide-details
              clearable
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row class="mt-n4 mx-2" v-if="!$vuetify.breakpoint.smAndUp">
          <v-col>
            <v-text-field
              :max-width="290"
              v-model="tab1.search"
              append-icon="mdi-magnify"
              label="Search"
              outlined
              dense
              hide-details
              clearable
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row class="font-weight-bold ml-3 mt-n2">
          <v-col> 총 매출액 : {{ tab1.totalSales }} </v-col>
          <v-col> 총 수익 : {{ tab1.totalIncome }} </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-data-table
              :loading="!!tab1.isLoading"
              loading-text="Loading... Please wait"
              v-model="tab1.selected"
              :headers="tab1.headers"
              :items="tab1.data"
              :sort-by="'order_time'"
              :sort-desc="false"
              :search="tab1.search"
              multi-sort
              item-key="order_id"
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
                <v-btn color="primary" @click="updateData">
                  Reset
                </v-btn>
              </template>
            </v-data-table>
          </v-col>
        </v-row>
      </v-tab-item>
      <v-tab-item>
        <v-row class="my-0 mx-2">
          <v-col cols="11" sm="5">
            <v-menu
              ref="menu"
              v-model="tab2.menu"
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
                  label="기간"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-if="!!tab2.month"
                v-model="date"
                :max="currentDate"
                type="month"
                no-title
                scrollable
              >
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="tab2.menu = false">
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="
                    () => {
                      $refs.menu.save(date);
                      this.updatePeriodData();
                    }
                  "
                >
                  OK
                </v-btn>
              </v-date-picker>
              <v-date-picker
                v-else
                :max="currentDate"
                v-model="date"
                no-title
                scrollable
              >
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="tab2.menu = false">
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="
                    () => {
                      $refs.menu.save(date);
                      this.updatePeriodData();
                    }
                  "
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
          </v-col>
          <v-col>
            <v-btn
              :disabled="!!tab2.day"
              class="white--text"
              color="teal"
              @click="selectType(0)"
            >
              일간
            </v-btn>
          </v-col>
          <v-col align="center">
            <v-btn
              :disabled="!!tab2.week"
              class="white--text"
              color="teal"
              @click="selectType(1)"
            >
              주간
            </v-btn>
          </v-col>
          <v-col align="end">
            <v-btn
              :disabled="!!tab2.month"
              class="white--text"
              color="teal"
              @click="selectType(2)"
            >
              월간
            </v-btn>
          </v-col>
        </v-row>
        <v-row class="mx-2">
          <v-col>
            <v-select
              v-model="tab2.select"
              :items="tab2.dropdown_item"
              item-text="name"
              item-value="value"
              label="표시 범위 선택"
              outlined
              @input="updatePeriodData"
              return-object
            ></v-select>
          </v-col>
          <v-col v-if="tab2.select.name == '직접 입력'">
            <v-text-field
              v-model="tab2.select.value"
              label="직접 입력"
              @change="updatePeriodData"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row v-if="!!tab2.isLoading">
          <v-alert outlined type="warning" prominent border="left">
            로딩중입니다......!
          </v-alert>
        </v-row>
        <v-row class="mx-2" v-else>
          <v-col>
            <line-chart :chart-data="tab2.datacollection"></line-chart>
          </v-col>
        </v-row>
      </v-tab-item>
      <v-tab-item>
        <v-row>
          <v-col>
            <v-alert v-if="!!errorMsg">{{ errorMsg }}</v-alert>
          </v-col>
        </v-row>
        <v-row class="mx-2">
          <v-col cols="11" sm="5">
            <v-menu
              ref="menu"
              v-model="tab3.menu"
              :close-on-content-click="false"
              :return-value.sync="tab3.dates"
              transition="scale-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="dateRangeText"
                  label="기간"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="tab3.dates"
                :max="currentDate"
                no-title
                range
              >
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="tab3.menu = false">
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="
                    () => {
                      $refs.menu.save(tab3.dates);
                      this.updateMenuData();
                    }
                  "
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>
          </v-col>
        </v-row>
        <v-row v-if="!!tab3.isLoading">
          <v-alert outlined type="warning" prominent border="left">
            로딩중입니다......!
          </v-alert>
        </v-row>
        <template v-else-if="!!tab3.salesDatacollection">
          <v-row class="text-center">
            <v-col> <p class="font-weight-bold title mb-n5">매출액</p></v-col>
          </v-row>
          <v-row class="mx-2 text-center">
            <v-col
              ><pie-chart
                :chart-data="tab3.salesDatacollection"
                :options="tab3.options"
              ></pie-chart>
            </v-col>
          </v-row>
          <v-row class="text-center">
            <v-col>
              <p class="font-weight-bold title mb-n5 mt-5">수익</p></v-col
            >
          </v-row>
          <v-row class="mx-2 text-center">
            <v-col
              ><pie-chart
                :chart-data="tab3.incomeDatacollection"
                :options="tab3.options"
              ></pie-chart>
            </v-col>
          </v-row>
        </template>
        <v-row v-else class="text-center">
          <v-col>데이터가 존재하지 않습니다.</v-col></v-row
        >
      </v-tab-item>
    </v-tabs>
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
import moment from "moment";
import axios from "axios";
import LineChart from "../components/LineChart";
import PieChart from "../components/PieChart";

export default {
  components: {
    LineChart,
    PieChart,
  },
  data() {
    return {
      tab: null,
      errorMsg: "",
      currentDate: moment().format("YYYY-MM-DD"),
      date: moment().format("YYYY-MM-DD"),
      tab1: {
        menu: false,
        isLoading: false,
        totalSales: null,
        totalIncome: null,
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
          { text: "수량", value: "order_num" },
        ],
      },
      tab2: {
        datacollection: null,
        menu: false,
        isLoading: false,
        day: true,
        week: false,
        month: false,
        labels: [],
        data: [],
        select: { name: "직접 입력", value: 7 },
        dropdown_item: [
          { name: "3개", value: 3 },
          { name: "7개", value: 7 },
          { name: "15개", value: 15 },
          { name: "직접 입력", value: 0 },
        ],
      },
      tab3: {
        menu: false,
        isLoading: false,
        salesDatacollection: null,
        incomeDatacollection: null,
        options: {
          plugins: {
            datalabels: {
              backgroundColor: function(context) {
                return context.dataset.backgroundColor;
              },
              borderColor: "white",
              borderRadius: 25,
              borderWidth: 2,
              color: "white",
            },
            display: function(context) {
              var dataset = context.dataset;
              var count = dataset.data.length;
              var value = dataset.data[context.dataIndex];
              return value > count * 1.5;
            },
            padding: 6,
          },
        },
        labels: [],
        salesData: [],
        incomeData: [],
        dates: [moment().format("YYYY-MM-DD"), moment().format("YYYY-MM-DD")],
      },
      snackbar: {
        show: false,
        timeout: 2000,
        text: "",
      },
    };
  },
  async created() {
    await this.updateData();
    await this.updatePeriodData();
  },
  computed: {
    dateRangeText() {
      return this.tab3.dates.join(" ~ ");
    },
  },
  methods: {
    async updateData() {
      //서버에서 data에 해당하는 날짜의 매출목록, 총매출액, 순이익을 불러온다.
      try {
        const res = await axios.get(
          `/order/sale?startDate=${this.date}&endDate=${this.date}`
        );
        this.tab1.totalSales = res.data.totalSales;
        this.tab1.totalIncome = res.data.totalIncome;
        this.tab1.data = res.data.data;
        this.tab1.data.forEach((val, idx) => {
          this.tab1.data[idx].order_time = moment(val.order_time).format(
            "YYYY/MM/DD HH:mm"
          );
          this.tab1.data[idx].order_type =
            val.order_type === false ? "출고" : "입고";
        });
      } catch (err) {
        this.showSnackbar("error", err.message);
      }
    },
    showSnackbar(color, text) {
      this.snackbar.show = true;
      this.snackbar.color = color;
      this.snackbar.text = text;
    },

    async updatePeriodData() {
      const addType = this.tab2.day
        ? "days"
        : this.tab2.week
        ? "weeks"
        : "months";
      let date = moment(this.date).format("YYYY-MM-DD");
      let startDate = moment(date)
        .clone()
        .subtract(this.tab2.select.value, addType)
        .format("YYYY-MM-DD");
      if (this.tab2.month) {
        startDate = moment(startDate)
          .add(1, "months")
          .startOf("month")
          .format("YYYY-MM-DD");
      }
      let endDate = moment(date)
        .add(1, addType)
        .format("YYYY-MM-DD");
      const res = await axios.get(
        `/order/sale?startDate=${startDate}&endDate=${endDate}&type=false`
      );
      if (this.tab2.month) startDate = moment(startDate);
      else {
        startDate = moment(
          moment(startDate)
            .add(1, "days")
            .format("YYYY-MM-DD")
        );
      }
      endDate = moment(endDate);
      this.tab2.labels = [];
      this.tab2.data = [];
      let idx = 0;
      let now;
      for (now = startDate; now < endDate && now <= moment(date); ) {
        let price = 0;
        const last = moment(
          now
            .clone()
            .add(1, addType)
            .format("YYYY-MM-DD")
        );
        let period = now.format("YYYY-MM-DD");
        for (
          ;
          now < last;
          now = moment(now.add(1, "days").format("YYYY-MM-DD"))
        ) {
          if (
            idx < res.data.length &&
            now.isSame(moment(res.data[idx].order_time), "day")
          ) {
            price += res.data[idx].order_sales;
            idx++;
          }
        }
        this.tab2.labels.push(period);
        this.tab2.data.push(price);
      }
      this.fillData();
    },
    async pickerUpdate() {
      await this.updateData();
    },
    async selectType(type) {
      this.tab2.day = type === 0;
      this.tab2.week = type === 1;
      this.tab2.month = type === 2;
      await this.updatePeriodData();
    },
    fillData() {
      this.tab2.datacollection = {
        labels: this.tab2.labels,
        datasets: [
          {
            label: "매출액",
            lineTension: 0,
            data: this.tab2.data,
            borderColor: "rgb(75, 192, 192)",
            fill: false,
          },
        ],
      };
    },

    async updateMenuData() {
      if (moment(this.tab3.dates[0]) > moment(this.tab3.dates[1])) {
        [this.tab3.dates[0], this.tab3.dates[1]] = [
          this.tab3.dates[1],
          this.tab3.dates[0],
        ];
      }
      let startDate = moment(this.tab3.dates[0]).format("YYYY-MM-DD");
      let endDate = moment(this.tab3.dates[1])
        .add(1, "days")
        .format("YYYY-MM-DD");
      const res = await axios.get(
        `/order/menu?startDate=${startDate}&endDate=${endDate}&type=false`
      );
      this.tab3.labels = [];
      this.tab3.salesData = [];
      this.tab3.incomeData = [];
      for (let item of res.data) {
        this.tab3.labels.push(item.product_name);
        this.tab3.salesData.push(item.order_sales);
        this.tab3.incomeData.push(item.order_sales - item.order_price);
      }
      this.fillTab3Data();
    },
    addComma(num) {
      var regexp = /\B(?=(\d{3})+(?!\d))/g;
      return num.toString().replace(regexp, ",");
    },
    fillTab3Data() {
      this.tab3.salesDatacollection = {
        labels: this.tab3.labels,
        datasets: [
          {
            label: "매출액",
            data: this.tab3.salesData,
            backgroundColor: [
              "#F26849",
              "#F2BF80",
              "#C3D9B8",
              "#B3D5F2",
              "#5A86BF",
              "#CB89A0",
            ],
            hoverOffset: 4,
          },
        ],
      };
      this.tab3.incomeDatacollection = {
        labels: this.tab3.labels,
        datasets: [
          {
            label: "수익",
            data: this.tab3.incomeData,
            backgroundColor: [
              "rgb(255, 99, 132)",
              "rgb(255, 159, 64)",
              "rgb(255, 205, 86)",
              "rgb(75, 192, 192)",
              "rgb(54, 162, 235)",
              "rgb(153, 102, 255)",
              "rgb(201, 203, 207)",
            ],
            hoverOffset: 4,
          },
        ],
      };
    },
  },
};
</script>
