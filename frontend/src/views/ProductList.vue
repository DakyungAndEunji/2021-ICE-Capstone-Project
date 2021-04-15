<template>
  <v-container>
    <v-row class="text-center">
      <v-col>
        <v-data-iterator
          :items="products"
          :search="search"
          :sort-by="sortBy.toLowerCase()"
          :sort-desc="sortDesc"
          hide-default-footer
        >
          <template v-slot:header>
            <v-toolbar clipped-left dark color="teal" class="mb-1">
              <v-menu
                v-if="!$vuetify.breakpoint.mdAndUp"
                :close-on-content-click="closeOnContentClick"
                offset-y
                :nudge-width="200"
              >
                <template v-slot:activator="{ on }">
                  <v-btn icon v-on="on">
                    <v-icon>mdi-tune-variant</v-icon>
                  </v-btn>
                </template>
                <v-card>
                  <v-list>
                    <v-list-item>
                      <v-select
                        v-model="sortBy"
                        flat
                        solo
                        hide-details
                        :items="keys"
                        item-text="text"
                        item-value="value"
                        prepend-inner-icon="mdi-magnify"
                        label="Sort by"
                      ></v-select>
                    </v-list-item>
                    <v-list-item class="d-flex justify-center">
                      <v-btn text outlined color="teal" :value="false">
                        오름차순
                      </v-btn>
                      <v-btn depressed color="teal" :value="true">
                        <v-icon color="white">mdi-arrow-down</v-icon>
                      </v-btn>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-menu>
              <v-text-field
                v-model="search"
                clearable
                flat
                solo-inverted
                hide-details
                prepend-inner-icon="mdi-magnify"
                label="Search"
              ></v-text-field>
              <template v-if="$vuetify.breakpoint.mdAndUp">
                <v-spacer></v-spacer>
                <v-select
                  v-model="sortBy"
                  flat
                  solo-inverted
                  hide-details
                  :items="keys"
                  item-text="text"
                  item-value="value"
                  prepend-inner-icon="mdi-magnify"
                  label="Sort by"
                ></v-select>
                <v-spacer></v-spacer>
                <v-btn-toggle v-model="sortDesc" mandatory>
                  <v-btn large depressed color="blue" :value="false">
                    <v-icon>mdi-arrow-up</v-icon>
                  </v-btn>
                  <v-btn large depressed color="blue" :value="true">
                    <v-icon>mdi-arrow-down</v-icon>
                  </v-btn>
                </v-btn-toggle>
              </template>
            </v-toolbar>
          </template>
          <template v-slot:default="props">
            <v-row>
              <v-col
                v-for="item in props.items"
                :key="item.product_name"
                cols="12"
                sm="6"
                md="4"
                lg="3"
              >
                <v-card>
                  <v-card-title class="subheading font-weight-bold">
                    {{ item.product_name }}<v-spacer />
                    <v-btn depressed @click="openProductUpdateDialog(item)">
                      <v-icon small>mdi-pencil</v-icon> 수정
                    </v-btn>
                  </v-card-title>

                  <v-divider></v-divider>

                  <v-list dense>
                    <v-list-item
                      v-for="(key, index) in filteredKeys"
                      :key="index"
                    >
                      <v-list-item-content
                        :class="{ 'blue--text': sortBy === key.value }"
                      >
                        {{ key.text }}:
                      </v-list-item-content>
                      <v-list-item-content
                        class="align-end"
                        :class="{ 'blue--text': sortBy === key.value }"
                      >
                        {{ item[key.value.toLowerCase()] }}
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>
            </v-row>
          </template>
        </v-data-iterator>
      </v-col>
    </v-row>

    <v-fab-transition>
      <v-btn
        color="teal mb-15 mr-3"
        fixed
        fab
        dark
        bottom
        right
        @click="openProductCreateDialog"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-fab-transition>
    <v-dialog v-if="dialog.show" v-model="dialog.show" max-width="350">
      <v-card class="overflow-hidden">
        <v-toolbar dark flat color="teal">
          <v-toolbar-title class="font-weight ma-2"
            >상품 정보 수정</v-toolbar-title
          >
          <v-spacer></v-spacer>
          <v-btn
            icon
            small
            class="mr-2"
            @click="dialog.isEditing = !dialog.isEditing"
          >
            <v-icon v-if="dialog.isEditing">mdi-close</v-icon>
            <v-icon v-else>mdi-pencil</v-icon>
          </v-btn>
        </v-toolbar>
        <v-container fluid>
          <v-card-text>
            <v-col>
              <v-row>
                <v-text-field
                  :disabled="!dialog.isEditing"
                  v-model="dialog.data.product_name"
                  label="상품명"
                ></v-text-field>
              </v-row>
              <v-row>
                <v-text-field
                  :disabled="!dialog.isEditing"
                  v-model="dialog.data.product_price"
                  label="원가"
                ></v-text-field>
              </v-row>
              <v-row>
                <v-text-field
                  :disabled="!dialog.isEditing"
                  v-model="dialog.data.product_sales"
                  label="판매가"
                ></v-text-field>
              </v-row>
              <v-row>
                <v-text-field
                  :disabled="!dialog.isEditing"
                  v-model="dialog.data.product_number"
                  label="상품재고"
                ></v-text-field>
              </v-row>
            </v-col>
          </v-card-text>
        </v-container>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="teal" @click="closeProductUpdateDialog" outlined>
            취소
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="teal" @click="deleteProduct" outlined>
            삭제
          </v-btn>
          <v-btn
            :disabled="!dialog.isEditing"
            color="teal"
            @click="update"
            outlined
          >
            저장
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-if="createDialog.show"
      v-model="createDialog.show"
      max-width="350"
    >
      <v-card class="overflow-hidden">
        <v-toolbar flat dark color="teal">
          <v-toolbar-title class="font-weight ma-2">상품 추가</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-container fluid>
          <v-card-text>
            <v-col>
              <v-row>
                <v-text-field
                  v-model="createDialog.data.product_name"
                  label="상품명"
                ></v-text-field>
              </v-row>
              <v-row>
                <v-text-field
                  v-model="createDialog.data.product_price"
                  label="원가"
                ></v-text-field>
              </v-row>
              <v-row>
                <v-text-field
                  v-model="createDialog.data.product_sales"
                  label="판매가"
                ></v-text-field>
              </v-row>
              <v-row>
                <v-text-field
                  v-model="createDialog.data.product_number"
                  label="상품재고"
                ></v-text-field>
              </v-row>
            </v-col>
          </v-card-text>
        </v-container>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="teal" @click="closeProductCreateDialog" outlined>
            취소
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="teal" @click="create" outlined>
            생성
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    closeOnContentClick: false,
    drawer: false,
    search: "",
    filter: {},
    sortDesc: false,
    sortBy: "product_name",
    keys: [
      { text: "이름", value: "product_name" },
      { text: "원가", value: "product_price" },
      { text: "판매가", value: "product_sales" },
      { text: "수량", value: "product_number" },
    ],
    products: [
      {
        product_name: "사랑에 빠진 딸기",
        product_price: "20000",
        product_sales: "80000",
        product_number: "3",
      },
      {
        product_name: "아몬드 봉봉봉",
        product_price: "30000",
        product_sales: "70000",
        product_number: "2",
      },
      {
        product_name: "레인보우 샤베트",
        product_price: "25000",
        product_sales: "65000",
        product_number: "2",
      },
    ],
    dialog: {
      title: "",
      show: false,
      isEditing: false,
      data: {
        product_name: "",
        product_price: "",
        product_sales: "",
        product_number: "",
      },
    },
    createDialog: {
      show: false,
      data: {
        product_name: "",
        product_price: "",
        product_sales: "",
        product_number: "",
      },
    },
  }),
  created() {
    // 재고 데이터 불러오기
  },
  computed: {
    filteredKeys() {
      return this.keys.filter((key) => key.value !== "product_name");
    },
  },
  methods: {
    create() {
      // 새로 생성한 재고 등록
    },
    submit() {
      // 수정된 재고 정보 서버에 전송
    },
    openProductUpdateDialog(item) {
      this.dialog.title = "상품 정보 수정";
      this.dialog.show = true;
      this.dialog.isEditing = false;
      this.dialog.data = {
        product_name: item.product_name,
        product_price: parseInt(item.product_price),
        product_sales: parseInt(item.product_sales),
        product_number: parseInt(item.product_number),
      };
    },
    closeProductUpdateDialog() {
      this.dialog.show = false;
      this.dialog.data = null;
    },
    openProductCreateDialog() {
      this.createDialog.data.product_state = true;
      this.createDialog.show = true;
    },
    closeProductCreateDialog() {
      this.createDialog.show = false;
    },
  },
};
</script>
