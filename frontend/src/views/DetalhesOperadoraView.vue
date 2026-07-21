<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { exibirDetalhesOperadora, listarDespesas } from "../services/api";

const route = useRoute();
const operadora = ref(null);
const despesas = ref([]);

async function carregarDetalhesOperadoras() {
  const cnpj = route.params.cnpj;
  const resposta = await exibirDetalhesOperadora(cnpj);

  operadora.value = resposta.data;
}

async function carregarDespesas() {
  const cnpj = route.params.cnpj;

  try {
    const resposta = await listarDespesas(cnpj);
    despesas.value = resposta.data;
  } finally {
    carregandoDespesas.value = false;
  }
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
  carregarDetalhesOperadoras();
  carregarDespesas();
});
</script>

<template>
  <main>
    <RouterLink to="/operadoras"> ← Voltar para a lista </RouterLink>

    <h1>Detalhes da Operadora</h1>

    <table v-if="operadora">
      <thead>
        <tr>
          <th>Registro ANS</th>
          <th>CNPJ</th>
          <th>Razão Social</th>
          <th>Modalidade</th>
          <th>UF</th>
        </tr>
      </thead>

      <tbody>
        <tr>
          <td>{{ operadora.registro_ans }}</td>
          <td>{{ formatarCnpj(operadora.cnpj) }}</td>
          <td>{{ operadora.razao_social }}</td>
          <td>{{ operadora.modalidade }}</td>
          <td>{{ operadora.uf }}</td>
        </tr>
      </tbody>
    </table>

    <h2>Despesas</h2>

    <p v-if="carregandoDespesas">Carregando despesas...</p>

    <table v-if="despesas.length > 0">
      <thead>
        <tr>
          <th>CNPJ</th>
          <th>Razão Social</th>
          <th>Ano</th>
          <th>Trimestre</th>
          <th>Valor das Despesas</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="despesa in despesas" :key="despesa.id">
          <td>{{ formatarCnpj(despesa.cnpj) }}</td>
          <td>{{ despesa.razao_social }}</td>
          <td>{{ despesa.ano }}</td>
          <td>{{ despesa.trimestre }}</td>
          <td>{{ formatarMoeda(despesa.valor_despesas) }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>Dados não encontrados.</p>
  </main>
</template>
