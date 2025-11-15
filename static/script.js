 async function atualizarClima() {
            try {
                const res = await fetch("/clima");
                const data = await res.json();

                document.getElementById("cidade").innerText = `Cidade: ${data.cidade}`;
                document.getElementById("temperatura").innerText = `${data.temperatura_agora} °C`;
            } catch (err) {
                console.error("Erro ao acessar API:", err);
                document.getElementById("cidade").innerText = "Erro ao carregar dados";
            }
        }

        async function analisarIA() {
            const boxIA = document.getElementById("analiseIA");
            boxIA.style.display = "block";
            boxIA.innerText = "Analisando...";

            try {
                const res = await fetch("/clima-ia");
                const data = await res.json();

                boxIA.innerText = data.analise_da_ia;
            } catch (err) {
                console.error("Erro IA:", err);
                boxIA.innerText = "Erro ao gerar análise da IA.";
            }
        }

        atualizarClima();
        setInterval(atualizarClima, 60000);