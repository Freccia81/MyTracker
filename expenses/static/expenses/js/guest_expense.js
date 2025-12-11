// static/expenses/js/guest_expense.js

document.addEventListener('DOMContentLoaded', () => {
    console.log('guest_expense.js caricato');  // debug

    const form = document.getElementById('guest-form');
    const list = document.getElementById('guest-list');
    const totalEl = document.getElementById('guest-total');
    const countEl = document.getElementById('expense-count');
    const emptyState = document.getElementById('empty-state');

    // Se per qualche motivo non troviamo gli elementi, usciamo
    if (!form || !list || !totalEl || !countEl || !emptyState) {
        console.warn('Elementi della home demo non trovati');
        return;
    }

    // Carica spese dal LocalStorage
    const loadExpenses = () => {
        const stored = localStorage.getItem('guest_expenses');
        return stored ? JSON.parse(stored) : [];
    };

    // Salva spese nel LocalStorage
    const saveExpenses = (expenses) => {
        localStorage.setItem('guest_expenses', JSON.stringify(expenses));
    };

    // Rendering tabella
    const render = () => {
        const expenses = loadExpenses();
        list.innerHTML = '';
        let total = 0;

        if (expenses.length === 0) {
            emptyState.classList.remove('hidden');
        } else {
            emptyState.classList.add('hidden');
        }

        [...expenses].reverse().forEach((ex) => {
            total += Number(ex.amount);

            const tr = document.createElement('tr');
            tr.className = 'hover:bg-gray-50 transition group';
            tr.innerHTML = `
                <td class="py-3 px-2 border-b border-gray-100 font-medium text-gray-800">
                    ${ex.desc}
                </td>
                <td class="py-3 px-2 border-b border-gray-100">
                    <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700">
                        ${ex.cat}
                    </span>
                </td>
                <td class="py-3 px-2 border-b border-gray-100 text-right font-mono text-gray-900 font-semibold">
                    € ${Number(ex.amount).toFixed(2)}
                </td>
                <td class="py-3 px-2 border-b border-gray-100 text-right">
                    <button class="delete-btn text-gray-300 hover:text-red-500 transition p-1 rounded-full hover:bg-red-50" data-id="${ex.id}" aria-label="Elimina">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    </button>
                </td>
            `;
            list.appendChild(tr);
        });

        totalEl.textContent = `€ ${total.toFixed(2)}`;
        countEl.textContent = `${expenses.length} moviment${expenses.length === 1 ? 'o' : 'i'}`;

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const button = e.currentTarget;
                const id = Number(button.dataset.id);
                deleteExpense(id);
            });
        });
    };

    const addExpense = (desc, amount, cat) => {
        const expenses = loadExpenses();
        const newExpense = {
            id: Date.now(),
            desc: desc,
            amount: amount,
            cat: cat,
            date: new Date().toISOString()
        };
        expenses.push(newExpense);
        saveExpenses(expenses);
        render();
    };

    const deleteExpense = (id) => {
        let expenses = loadExpenses();
        expenses = expenses.filter(ex => ex.id !== id);
        saveExpenses(expenses);
        render();
    };

    // Gestione submit form
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const descInput = document.getElementById('desc');
        const amountInput = document.getElementById('amount');
        const catInput = document.getElementById('cat');

        // unico obbligatorio: importo
        if (!amountInput.value) {
            amountInput.focus();
            return;
        }

        const desc = (descInput.value || '').trim() || 'Senza descrizione';

        addExpense(desc, parseFloat(amountInput.value), catInput.value);

        form.reset();
        descInput.focus();
    });

    // Render iniziale
    render();
});
