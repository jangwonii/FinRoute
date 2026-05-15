const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export type ApiEnvelope<T> = {
  data: T;
  meta: Record<string, unknown>;
  errors: Array<{ code: string; field?: string | null; message: string }>;
};

export type Customer = {
  customer_id: string;
  advisor_id: string;
  name: string;
  birth_year: number | null;
  gender: string | null;
  occupation: string | null;
  household_type: string | null;
  memo: string | null;
  created_at: string;
  updated_at: string;
};

export type CustomerCreateInput = {
  name: string;
  birth_year?: number;
  occupation?: string;
  household_type?: string;
  memo?: string;
};

async function request<T>(path: string, init?: RequestInit): Promise<ApiEnvelope<T>> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });
  const envelope = (await response.json()) as ApiEnvelope<T>;
  if (!response.ok) {
    const message = envelope.errors[0]?.message ?? `Request failed with ${response.status}`;
    throw new Error(message);
  }
  return envelope;
}

export async function fetchHealth(): Promise<ApiEnvelope<{ status: string; service: string }>> {
  return request("/health");
}

export async function fetchCustomers(): Promise<ApiEnvelope<Customer[]>> {
  return request("/customers?page=1&page_size=25");
}

export async function createCustomer(
  input: CustomerCreateInput,
): Promise<ApiEnvelope<Customer>> {
  return request("/customers", {
    method: "POST",
    body: JSON.stringify(input),
  });
}
