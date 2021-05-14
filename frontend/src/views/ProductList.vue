<template>
  <v-container class="pa-0">
    <!-- 카드를 이용한 버전 -->
    <template v-if="!$vuetify.breakpoint.smAndUp">
      <v-data-iterator
        :items="products"
        :search="search"
        :sort-by="sortBy.toLowerCase()"
        :sort-desc="sortDesc"
        hide-default-footer
        class="mb-3"
      >
        <template v-slot:header>
          <v-toolbar dark color="teal" class="mb-1">
            <v-menu
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
                    <v-btn-toggle dense mandatory v-model="sortDesc">
                      <v-btn color="teal lighten-2" :value="false">
                        오름차순
                      </v-btn>
                      <v-btn color="teal lighten-2" :value="true">
                        내림차순
                      </v-btn>
                    </v-btn-toggle>
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
              <v-card class="mx-3">
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
    </template>
    <!-- data table을 이용한 버전(표) -->
    <template v-else>
      <v-toolbar dark color="teal" class="mb-1">
        <!-- 아이콘버전 -->
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="mx-3"
              small
              icon
              @click="openProductCreateDialog"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <span>상품 추가</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="mx-3"
              icon
              small
              @click="selectAllDelete"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
          <span>선택한 상품 삭제</span>
        </v-tooltip>
      </v-toolbar>
      <v-row class="mt-0 mx-2">
        <v-col>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
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
            :items="products"
            :sort-by="'product_name'"
            :sort-desc="true"
            :search="search"
            multi-sort
            item-key="product_name"
            show-select
            class="elevation-1"
          >
            <template v-slot:[`item.actions`]="{ item }">
              <v-icon small class="mr-2" @click="openProductUpdateDialog(item)">
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
    </template>
    <v-fab-transition v-if="!$vuetify.breakpoint.smAndUp">
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
          <v-toolbar-title class="font-weight ma-2">
            상품 정보 수정
          </v-toolbar-title>
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
                  v-model="dialog.data.product_num"
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
          <v-btn color="teal" @click="deleteItem(dialog.data)" outlined>
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
                  v-model="createDialog.data.product_num"
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
    <v-dialog v-model="dialogDelete" max-width="500px">
      <v-card>
        <v-card-title class="justify-center">
          상품을 삭제하시겠습니까?
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDelete">취소</v-btn>
          <v-btn color="blue darken-1" text @click="deleteProduct">
            확인
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
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
    //////// 카드형으로 만들때 사용하는 data /////////
    closeOnContentClick: false,
    drawer: false,
    filter: {},
    sortDesc: false,
    sortBy: "product_name",
    keys: [
      { text: "이름", value: "product_name" },
      { text: "원가", value: "product_price" },
      { text: "판매가", value: "product_sales" },
      { text: "수량", value: "product_num" },
    ],
    /////////////////////////////////////////////////

    ///// data table형으로 만들 때 사용하는 data /////
    isLoading: false,
    dialogDelete: false,
    selected: [],
    headers: [
      { text: "이름", align: "start", value: "product_name" },
      { text: "원가", value: "product_price" },
      { text: "판매가", value: "product_sales" },
      { text: "수량", value: "product_num" },
      { text: "편집", value: "actions", sortable: false },
    ],
    /////////////////////////////////////////////////

    iconVer: true,

    search: "",
    products: [],
    dialog: {
      title: "",
      show: false,
      isEditing: false,
      data: {
        product_id: "",
        product_name: "",
        product_price: "",
        product_sales: "",
        product_num: "",
      },
    },
    createDialog: {
      show: false,
      data: {
        product_name: "",
        product_price: "",
        product_sales: "",
        product_num: "",
      },
    },
    snackbar: {
      show: false,
      timeout: 2000,
      text: "",
    },
  }),
  async created() {
    // 재고 데이터 불러오기
    this.initialize();
  },
  computed: {
    filteredKeys() {
      return this.keys.filter((key) => key.value !== "product_name");
    },
  },
  methods: {
    async create() {
      // 새로 생성한 재고 등록
      try {
        await axios.post("/product", this.createDialog.data);
        await this.initialize();
        this.showSnackbar("success", "상품 생성에 성공했습니다.");
        this.createDialog.show = false;
        console.log(this.createDialog.show);
      } catch (err) {
        this.showSnackbar("error", err.message);
      }
    },
    async update() {
      // 수정된 재고 정보 서버에 전송
      try {
        const res = await axios.patch(
          `/product/${this.dialog.data.product_id}`,
          this.dialog.data
        );
        console.log(res.data);
        await this.initialize();
        this.showSnackbar("success", "상품 수정에 성공했습니다.");
        this.dialog.show = false;
        this.dialog.data = null;
      } catch (err) {
        this.showSnackbar("error", err.message);
      }
    },
    async deleteProduct() {
      // 선택한 제고 삭제
      this.isLoading = true;
      try {
        if (
          typeof this.selected !== "undefined" &&
          this.selected.length === 0
        ) {
          await axios.delete(`/product/${this.dialog.data.product_id}`);
        } else {
          for (const val of this.selected) {
            await await axios.delete(`/product/${val.product_id}`);
          }
          this.selected = [];
        }
        await this.initialize();
        this.showSnackbar("success", "상품 삭제를 성공했습니다.");
        this.closeDelete();
      } catch (err) {
        this.showSnackbar("error", err.message);
      }
      this.isLoading = false;
    },
    async initialize() {
      const res = await axios.get("/product");
      this.products = res.data;
    },
    openProductUpdateDialog(item) {
      this.dialog.title = "상품 정보 수정";
      this.dialog.show = true;
      this.dialog.isEditing = false;
      this.dialog.data = Object.assign({}, item);
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
    deleteItem(item) {
      //this.editedIndex = this.desserts.indexOf(item);
      this.closeProductUpdateDialog();
      this.dialog.data = Object.assign({}, item);
      this.dialogDelete = true;
    },
    closeDelete() {
      this.dialogDelete = false;
    },
    selectAllDelete() {
      if (
        (this.selected && this.selected.length) < 1 ||
        this.selected[0] === null
      ) {
        this.showSnackbar("error", "선택된 상품이 없습니다!");
        return;
      }
      // 선택한 모든 상품을 삭제
      this.deleteItem(this.selected[0]);
    },
    showSnackbar(color, text) {
      this.snackbar.show = true;
      this.snackbar.color = color;
      this.snackbar.text = text;
    },
  },
};
</script>
