<script setup>
import { computed, onMounted, ref } from "vue"
import { exibirEstatisticas } from "../services/api"
import { Bar } from "vue-chartjs"

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from "chart.js"

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
)

const carregando = ref(true)
const erro = ref("")
const estatisticas = ref(null)

async function carregarEstatisticas() {
  carregando.value = true
  erro.value = ""

  try {
    const resposta = await exibirEstatisticas()
    estatisticas.value = resposta
  } catch (error) {
    console.error(error)
    erro.value = "Não foi possível carregar as estatísticas."
  } finally {
    carregando.value = false
  }
}

function formatarMoeda(valor) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL"
  }).format(valor)
}

function formatarCnpj(cnpj) {
  const texto = cnpj.toString()

  return texto.replace(
    /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
    "$1.$2.$3/$4-$5"
  )
}

const dadosGrafico = computed(() => {
  if (!estatisticas.value) {
    return {
      labels: [],
      datasets: []
    }
  }

  return {
    labels: estatisticas.value.distribuicao_uf.map((item) => item.uf),

    datasets: [
      {
        label: "Total de despesas por UF",
        data: estatisticas.value.distribuicao_uf.map(
          (item) => Number(item.total_despesas_uf)
        ),
        backgroundColor: "#111827",
        minBarLength: 5
      }
    ]
  }
})

const opcoesGrafico = {
  responsive: true,
  maintainAspectRatio: false,

  plugins: {
    legend: {
      display: false
    },

    tooltip: {
      callbacks: {
        label(contexto) {
          return `Total: ${formatarMoeda(contexto.raw)}`
        }
      }
    }
  },

  scales: {
    y: {
      beginAtZero: true,

      ticks: {
        callback(valor) {
          return new Intl.NumberFormat("pt-BR", {
            notation: "compact"
          }).format(valor)
        }
      }
    },

    x: {
      ticks: {
        autoSkip: false
      }
    }
  }
}

onMounted(() => {
  carregarEstatisticas()
})
</script>

<template>
  <main>
    <h1>Dashboard</h1>

    <p v-if="carregando" class="mensagem-loading">
      Carregando estatísticas...
    </p>

    <p v-else-if="erro" class="mensagem-erro">
      {{ erro }}
    </p>

    <div v-else-if="estatisticas">
      <div class="cards-estatisticas">
        <div class="card-estatistica">
          <span>Total de despesas</span>

          <strong>
            {{ formatarMoeda(estatisticas.total_despesas) }}
          </strong>
        </div>

        <div class="card-estatistica">
          <span>Média de despesas</span>

          <strong>
            {{ formatarMoeda(estatisticas.media_despesas) }}
          </strong>
        </div>
      </div>

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
          <tr v-for="operadora in estatisticas.top_operadoras" :key="operadora.cnpj">
            <td>{{ formatarCnpj(operadora.cnpj) }}</td>
            <td>{{ operadora.razao_social }}</td>
            <td>{{ formatarMoeda(operadora.total_despesas) }}</td>
          </tr>
        </tbody>
      </table>

      <h3>Distribuição de Despesas por UF</h3>

      <div class="grafico">
        <Bar :data="dadosGrafico" :options="opcoesGrafico" />
      </div>

    </div>

    <p v-else class="mensagem-vazia">
      Nenhuma estatística encontrada.
    </p>
  </main>
</template>