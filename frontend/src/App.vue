<script setup>
import OperadorasView from "./views/OperadorasView.vue";
import estatisticasView from "./views/EstatisticasView.vue";
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Dashboard</RouterLink>
      <RouterLink to="/operadoras">Operadoras</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>
