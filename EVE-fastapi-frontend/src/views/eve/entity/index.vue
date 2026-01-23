<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="组织名称" prop="entityName">
        <el-input
          v-model="queryParams.entityName"
          placeholder="请输入组织名称"
          clearable
          style="width: 200px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="组织状态" clearable style="width: 200px">
          <el-option
            v-for="dict in sys_normal_disable"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="授权" prop="isAuthorized">
        <el-select v-model="queryParams.isAuthorized" placeholder="授权状态" clearable style="width: 200px">
          <el-option label="未授权" value="0" />
          <el-option label="已授权" value="1" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['eve:entity:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="Sort"
          @click="toggleExpandAll"
        >展开/折叠</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table
      v-if="refreshTable"
      v-loading="loading"
      :data="entityList"
      row-key="entityId"
      :default-expand-all="isExpandAll"
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
    >
      <el-table-column prop="entityName" label="组织名称" width="220"></el-table-column>
      <el-table-column prop="ticker" label="简称" width="120"></el-table-column>
      <el-table-column prop="icon" label="图标" width="120">
        <template #default="scope">
          <el-avatar :size="28" :src="scope.row.icon" icon="Picture" />
        </template>
      </el-table-column>
      <el-table-column prop="entityType" label="类型" width="120">
        <template #default="scope">
          <span>{{ renderEntityType(scope.row.entityType) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="ceoId" label="CEO/执行官" width="160"></el-table-column>
      <el-table-column prop="isAuthorized" label="授权" width="120">
        <template #default="scope">
          <el-switch
            v-model="scope.row.isAuthorized"
            active-value="1"
            inactive-value="0"
            active-text="已授权"
            inactive-text="未授权"
            @change="val => handleAuthorizedChange(val, scope.row)"
            inline-prompt
          />
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <dict-tag :options="sys_normal_disable" :value="scope.row.status" />
        </template>
      </el-table-column>
      <el-table-column prop="orderNum" label="排序" width="100"></el-table-column>
      <el-table-column label="创建时间" align="center" prop="createTime" width="200">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createTime) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['eve:entity:edit']">修改</el-button>
          <el-button link type="primary" icon="Plus" @click="handleAdd(scope.row)" v-hasPermi="['eve:entity:add']">新增</el-button>
          <el-button v-if="scope.row.parentId != 0" link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['eve:entity:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="title" v-model="open" width="720px" append-to-body>
      <el-form ref="entityRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="12">
          <el-col :span="24" v-if="form.parentId !== 0">
            <el-form-item label="上级组织" prop="parentId">
              <el-tree-select
                v-model="form.parentId"
                :data="entityOptions"
                :props="{ value: 'entityId', label: 'entityName', children: 'children' }"
                value-key="entityId"
                placeholder="选择上级组织"
                check-strictly
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="组织名称" prop="entityName">
              <el-input v-model="form.entityName" placeholder="请输入组织名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="简称" prop="ticker">
              <el-input v-model="form.ticker" placeholder="请输入简称" maxlength="20" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="类型" prop="entityType">
              <el-radio-group v-model="form.entityType">
                <el-radio value="1">联盟</el-radio>
                <el-radio value="2">军团</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="显示排序" prop="orderNum">
              <el-input-number v-model="form.orderNum" controls-position="right" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="CEO/执行官" prop="ceoId">
              <el-input v-model="form.ceoId" placeholder="请输入CEO/执行官ID" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="授权" prop="isAuthorized">
              <el-switch
                v-model="form.isAuthorized"
                active-value="1"
                inactive-value="0"
                active-text="已授权"
                inactive-text="未授权"
                inline-prompt
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="图标URL" prop="icon">
              <el-input v-model="form.icon" placeholder="请输入图标地址" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="组织状态" prop="status">
              <el-radio-group v-model="form.status">
                <el-radio
                  v-for="dict in sys_normal_disable"
                  :key="dict.value"
                  :value="dict.value"
                >{{ dict.label }}</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="备注" prop="remark">
              <el-input v-model="form.remark" type="textarea" placeholder="请输入备注" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="EveEntity">
import { listEntity, getEntity, delEntity, addEntity, updateEntity, listEntityExcludeChild } from "@/api/eve/entity";

const { proxy } = getCurrentInstance();
const { sys_normal_disable } = proxy.useDict("sys_normal_disable");

const entityList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const title = ref("");
const entityOptions = ref([]);
const isExpandAll = ref(true);
const refreshTable = ref(true);

const data = reactive({
  form: {},
  queryParams: {
    entityName: undefined,
    status: undefined,
    isAuthorized: undefined
  },
  rules: {
    parentId: [{ required: true, message: "上级组织不能为空", trigger: "blur" }],
    entityName: [{ required: true, message: "组织名称不能为空", trigger: "blur" }],
    orderNum: [{ required: true, message: "显示排序不能为空", trigger: "blur" }]
  }
});

const { queryParams, form, rules } = toRefs(data);

function renderEntityType(type) {
  if (type === "1") return "联盟";
  if (type === "2") return "军团";
  return "";
}

function buildPayload(row) {
  const { entityId, parentId, entityName, ticker, entityType, isAuthorized, icon, orderNum, status, ceoId, executorCorpId, remark } = row;
  return { entityId, parentId, entityName, ticker, entityType, isAuthorized, icon, orderNum, status, ceoId, executorCorpId, remark };
}

/** 查询组织列表 */
function getList() {
  loading.value = true;
  listEntity(queryParams.value).then(response => {
    entityList.value = proxy.handleTree(response.data, "entityId");
    loading.value = false;
  });
}
/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}
/** 表单重置 */
function reset() {
  form.value = {
    entityId: undefined,
    parentId: undefined,
    entityName: undefined,
    ticker: undefined,
    entityType: "2",
    orderNum: 0,
    ceoId: undefined,
    executorCorpId: undefined,
    isAuthorized: "0",
    icon: undefined,
    status: "0",
    remark: undefined
  };
  proxy.resetForm("entityRef");
}
/** 搜索按钮操作 */
function handleQuery() {
  getList();
}
/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}
/** 新增按钮操作 */
function handleAdd(row) {
  reset();
  listEntity().then(response => {
    entityOptions.value = proxy.handleTree(response.data, "entityId");
  });
  if (row !== undefined) {
    form.value.parentId = row.entityId;
  }
  open.value = true;
  title.value = "添加组织";
}
/** 展开/折叠操作 */
function toggleExpandAll() {
  refreshTable.value = false;
  isExpandAll.value = !isExpandAll.value;
  nextTick(() => {
    refreshTable.value = true;
  });
}
/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  listEntityExcludeChild(row.entityId).then(response => {
    entityOptions.value = proxy.handleTree(response.data, "entityId");
  });
  getEntity(row.entityId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改组织";
  });
}
/** 授权开关 */
function handleAuthorizedChange(value, row) {
  const payload = buildPayload({ ...row, isAuthorized: value });
  updateEntity(payload).then(() => {
    proxy.$modal.msgSuccess("授权状态已更新");
    getList();
  }).catch(() => {
    getList();
  });
}
/** 提交按钮 */
function submitForm() {
  proxy.$refs["entityRef"].validate(valid => {
    if (valid) {
      if (form.value.entityId !== undefined) {
        updateEntity(buildPayload(form.value)).then(() => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addEntity(buildPayload(form.value)).then(() => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}
/** 删除按钮操作 */
function handleDelete(row) {
  proxy.$modal.confirm('是否确认删除名称为"' + row.entityName + '"的数据项?').then(function() {
    return delEntity(row.entityId);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

getList();
</script>
