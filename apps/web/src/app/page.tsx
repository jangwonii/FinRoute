"use client";

import { FormEvent, useEffect, useState } from "react";

import {
  Customer,
  CustomerCreateInput,
  createCustomer,
  fetchCustomers,
  fetchHealth,
} from "@/lib/api";

type FormState = {
  name: string;
  birth_year: string;
  occupation: string;
  household_type: string;
  memo: string;
};

const emptyForm: FormState = {
  name: "",
  birth_year: "",
  occupation: "",
  household_type: "",
  memo: "",
};

const workflowSteps = [
  { label: "Customer", status: "Active", detail: "Create and list advisor-owned customer records." },
  { label: "Statement", status: "Next", detail: "Upload and review standard Excel v1 data." },
  { label: "Diagnosis", status: "Waiting", detail: "Generate deterministic metrics and issue tags." },
  { label: "Allocation", status: "Waiting", detail: "Review rule-based monthly allocation items." },
];

export default function Home() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [form, setForm] = useState<FormState>(emptyForm);
  const [apiStatus, setApiStatus] = useState("Checking");
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadCustomers() {
    setError(null);
    setIsLoading(true);
    try {
      const [healthEnvelope, customersEnvelope] = await Promise.all([
        fetchHealth(),
        fetchCustomers(),
      ]);
      setApiStatus(healthEnvelope.data.status);
      setCustomers(customersEnvelope.data);
    } catch (caught) {
      setApiStatus("Unavailable");
      setError(caught instanceof Error ? caught.message : "Failed to load customers");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadCustomers();
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    const payload: CustomerCreateInput = {
      name: form.name.trim(),
      occupation: form.occupation.trim() || undefined,
      household_type: form.household_type.trim() || undefined,
      memo: form.memo.trim() || undefined,
    };

    if (form.birth_year.trim()) {
      payload.birth_year = Number(form.birth_year);
    }

    setIsSubmitting(true);
    try {
      await createCustomer(payload);
      setForm(emptyForm);
      await loadCustomers();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Failed to create customer");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="min-h-screen">
      <header className="border-b border-[var(--line)] bg-[var(--panel)]">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div>
            <p className="text-sm font-medium text-[var(--muted)]">FinRoute</p>
            <h1 className="text-2xl font-semibold">Advisor Workflow</h1>
          </div>
          <div className="rounded-md border border-[var(--line)] px-3 py-2 text-sm text-[var(--muted)]">
            API {apiStatus}
          </div>
        </div>
      </header>

      <section className="mx-auto grid max-w-7xl gap-6 px-6 py-8 lg:grid-cols-[1.3fr_0.9fr]">
        <div className="space-y-6">
          <div className="border-b border-[var(--line)] pb-4">
            <p className="text-sm font-medium text-[var(--accent)]">Customer workspace</p>
            <h2 className="mt-2 text-3xl font-semibold">Start from advisor-owned customers</h2>
            <p className="mt-3 max-w-3xl text-base leading-7 text-[var(--muted)]">
              Customer records are the first persistent slice for statement upload, diagnosis,
              allocation review, product recommendation, and report export.
            </p>
          </div>

          <section className="rounded-md border border-[var(--line)] bg-[var(--panel)]">
            <div className="flex items-center justify-between border-b border-[var(--line)] px-4 py-3">
              <h3 className="text-lg font-semibold">Customers</h3>
              <button
                type="button"
                onClick={() => void loadCustomers()}
                className="rounded-md border border-[var(--line)] px-3 py-2 text-sm text-[var(--muted)] hover:border-[var(--accent)] hover:text-[var(--accent)]"
              >
                Refresh
              </button>
            </div>

            {error ? (
              <div className="border-b border-[#e2c48e] bg-[#fff8ea] px-4 py-3 text-sm text-[#6f4b12]">
                {error}
              </div>
            ) : null}

            <div className="divide-y divide-[var(--line)]">
              {isLoading ? (
                <p className="px-4 py-6 text-sm text-[var(--muted)]">Loading customers...</p>
              ) : customers.length === 0 ? (
                <p className="px-4 py-6 text-sm text-[var(--muted)]">
                  No customers yet. Create the first record to begin the workflow.
                </p>
              ) : (
                customers.map((customer) => (
                  <article
                    key={customer.customer_id}
                    className="grid gap-3 px-4 py-4 md:grid-cols-[1fr_auto]"
                  >
                    <div>
                      <h4 className="font-semibold">{customer.name}</h4>
                      <p className="mt-1 text-sm text-[var(--muted)]">
                        {[customer.occupation, customer.household_type, customer.birth_year]
                          .filter(Boolean)
                          .join(" / ") || "Basic profile only"}
                      </p>
                      {customer.memo ? (
                        <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{customer.memo}</p>
                      ) : null}
                    </div>
                    <span className="h-fit rounded-md bg-[#e8f2ed] px-2 py-1 text-xs text-[var(--accent-strong)]">
                      Ready
                    </span>
                  </article>
                ))
              )}
            </div>
          </section>
        </div>

        <aside className="space-y-4">
          <section className="rounded-md border border-[var(--line)] bg-[var(--panel)] p-4">
            <h2 className="text-lg font-semibold">Create Customer</h2>
            <form className="mt-4 space-y-3" onSubmit={handleSubmit}>
              <label className="block text-sm">
                <span className="font-medium">Name</span>
                <input
                  required
                  value={form.name}
                  onChange={(event) => setForm({ ...form, name: event.target.value })}
                  className="mt-1 w-full rounded-md border border-[var(--line)] px-3 py-2 outline-none focus:border-[var(--accent)]"
                  placeholder="Customer name"
                />
              </label>
              <label className="block text-sm">
                <span className="font-medium">Birth year</span>
                <input
                  value={form.birth_year}
                  onChange={(event) => setForm({ ...form, birth_year: event.target.value })}
                  className="mt-1 w-full rounded-md border border-[var(--line)] px-3 py-2 outline-none focus:border-[var(--accent)]"
                  inputMode="numeric"
                  placeholder="1988"
                />
              </label>
              <label className="block text-sm">
                <span className="font-medium">Occupation</span>
                <input
                  value={form.occupation}
                  onChange={(event) => setForm({ ...form, occupation: event.target.value })}
                  className="mt-1 w-full rounded-md border border-[var(--line)] px-3 py-2 outline-none focus:border-[var(--accent)]"
                  placeholder="Engineer"
                />
              </label>
              <label className="block text-sm">
                <span className="font-medium">Household type</span>
                <input
                  value={form.household_type}
                  onChange={(event) => setForm({ ...form, household_type: event.target.value })}
                  className="mt-1 w-full rounded-md border border-[var(--line)] px-3 py-2 outline-none focus:border-[var(--accent)]"
                  placeholder="single"
                />
              </label>
              <label className="block text-sm">
                <span className="font-medium">Memo</span>
                <textarea
                  value={form.memo}
                  onChange={(event) => setForm({ ...form, memo: event.target.value })}
                  className="mt-1 min-h-24 w-full rounded-md border border-[var(--line)] px-3 py-2 outline-none focus:border-[var(--accent)]"
                  placeholder="Advisor note"
                />
              </label>
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full rounded-md bg-[var(--accent)] px-3 py-2 font-medium text-white hover:bg-[var(--accent-strong)] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isSubmitting ? "Creating..." : "Create Customer"}
              </button>
            </form>
          </section>

          <section className="rounded-md border border-[var(--line)] bg-[var(--panel)] p-4">
            <h2 className="text-lg font-semibold">Workflow</h2>
            <div className="mt-4 space-y-3">
              {workflowSteps.map((step, index) => (
                <div key={step.label} className="flex items-start justify-between gap-3 text-sm">
                  <div>
                    <p className="font-medium">
                      {index + 1}. {step.label}
                    </p>
                    <p className="mt-1 text-[var(--muted)]">{step.detail}</p>
                  </div>
                  <span className="rounded-md border border-[var(--line)] px-2 py-1 text-xs text-[var(--muted)]">
                    {step.status}
                  </span>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-md border border-[#e2c48e] bg-[#fff8ea] p-4">
            <h2 className="text-lg font-semibold text-[var(--warning)]">Release Gate Reminder</h2>
            <p className="mt-2 text-sm leading-6 text-[#6f4b12]">
              Parser, recommendation, RAG, and report export can be prototyped, but production
              release remains blocked until compliance, Excel template, product DB, and document
              ownership gates are complete.
            </p>
          </section>
        </aside>
      </section>
    </main>
  );
}
