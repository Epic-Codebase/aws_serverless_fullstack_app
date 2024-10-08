<script setup>
  import { Authenticator } from '@aws-amplify/ui-vue';
  import { reactive, onMounted } from "vue";
  import { Auth } from '@aws-amplify/auth';
  import '@aws-amplify/ui-vue/styles.css';
  import axios from 'axios';

  const API_URL = import.meta.env.VITE_VUE_APP_API_URL || 'http://localhost:8000/api';

  const createTaskForm = reactive({ title: '' });

  const tasks = reactive({openTasks: [], closedTasks: []});

  const createTask = async () => {
    const { idToken } = await Auth.currentSession();

    const config = {headers: {Authorization: idToken.getJwtToken()}};
    await axios.post(`${API_URL}/create-task`, {title: createTaskForm.title}, config);
    createTaskForm.title = '';
    await listOpenTasks();
  }

  const listOpenTasks = async () => {
    const { idToken } = await Auth.currentSession();

    const config = {headers: {Authorization: idToken.getJwtToken()}};
    const response = await axios.get(`${API_URL}/open-tasks`, config);
    tasks.openTasks = response.data.results;
  }
  const listClosedTasks = async () => {
    const { idToken } = await Auth.currentSession();

    const config = {headers: {Authorization: idToken.getJwtToken()}};
    const response = await axios.get(`${API_URL}/closed-tasks`, config);
    tasks.closedTasks = response.data.results;
  }
  const closeTask = async (id) => {
    const { idToken } = await Auth.currentSession();

    const config = {headers: {Authorization: idToken.getJwtToken()}};
    await axios.post(`${API_URL}/close-task`, {id: id}, config);
    await listOpenTasks();
    await listClosedTasks();
  }
  onMounted(() => {
    listOpenTasks();
    listClosedTasks();
  })

</script>
<template>
  <authenticator username-alias="email" :login-mechanisms="['email']">
    <template v-slot="{ signOut }">
        <el-menu
          class="el-menu"
          mode="horizontal"
          :ellipsis="false"
        >
          <div class="flex-grow" />
          <el-menu-item index="0" @click="signOut">Sign Out</el-menu-item>
        </el-menu>
        <el-row>
          <el-col :span="8" :offset="8">
            <el-card class="box-card">
              <el-form :model="createTaskForm" label-width="120px">
                  <el-form-item label="Task Title">
                    <el-input v-model="createTaskForm.title" />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="createTask">Create</el-button>
                  </el-form-item>
                </el-form>
            </el-card>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-card class="box-card">
              <template #header>
                <div class="card-header">
                  <span>Open tasks</span>
                </div>
              </template>
              <el-table :data="tasks.openTasks">
                <el-table-column prop="title" label="Title" />
                <el-table-column fixed="right" label="Actions" width="120">
                  <template #default="scope">
                    <el-button link type="primary" size="large" @click="closeTask(scope.row.id)">Close</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="box-card">
              <template #header>
                <div class="card-header">
                  <span>Closed tasks</span>
                </div>
              </template>
              <el-table :data="tasks.closedTasks">
                <el-table-column prop="title" label="Title" />
              </el-table>
            </el-card>
          </el-col>
        </el-row>
    </template>
  </authenticator>
</template>


<style lang="scss">
.flex-grow {
  flex-grow: 1;
}
</style>