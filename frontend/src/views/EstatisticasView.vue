<script setup>
import { onMounted, ref } from "vue";
import { exibirEstatisticas } from "../services/api";

const estatisticas = ref(null);

async function carregarEstatisticas() {
  const resposta = await exibirEstatisticas();

  estatisticas.value = resposta;
}

function formatarMoeda(valor) {
  return Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(valor);
}

function formatarCnpj(cnpj) {
  const texto = cnpj.toString();

  return texto.replace(
    /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
    "$1.$2.$3/$4-$5",
  );
}

onMounted(() => {
  carregarEstatisticas();
});
</script>

<template>
  <main>
    <h1>Dashboard</h1>

    <div v-if="estatisticas">
      <p>Total de despesas: {{ formatarMoeda(estatisticas.total_despesas) }}</p>
      <p>Média de despesas: {{ formatarMoeda(estatisticas.media_despesas) }}</p>

      <h3>Top 5 Operadoras por Despesas</h3>
      <table>
        <thead>
          <tr>
            <th>CNPJ</th>
            <th>Razão Social</th>
            <th>Total de Despesas</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="operadora in estatisticas.top_operadoras"
            :key="operadora.cnpj"
          >
            <td>{{ formatarCnpj(operadora.cnpj) }}</td>
            <td>{{ operadora.razao_social }}</td>
            <td>{{ formatarMoeda(operadora.total_despesas) }}</td>
          </tr>
        </tbody>
      </table>

      <h3>Distribuição de Despesas por UF</h3>
      <table>
        <thead>
          <tr>
            <th>UF</th>
            <th>Total de Despesas</th>
            <th>Media de despesas</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="uf in estatisticas.distribuicao_uf" :key="uf.uf">
            <td>{{ uf.uf }}</td>
            <td>{{ formatarMoeda(uf.total_despesas_uf) }}</td>
            <td>{{ formatarMoeda(uf.media_despesas_por_operadora) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else>Carregando estatísticas...</p>
  </main>
</template>
