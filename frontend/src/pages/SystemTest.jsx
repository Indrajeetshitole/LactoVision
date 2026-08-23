import { useEffect, useState } from "react";
import { createTestRecord, getTestRecords } from "../services/api";

export default function SystemTest() {
  const [message, setMessage] = useState("Phase 1 MongoDB connection test");
  const [records, setRecords] = useState([]);
  const [status, setStatus] = useState("");

  async function loadRecords() {
    try {
      setRecords(await getTestRecords());
    } catch (err) {
      setStatus(err?.response?.data?.detail || "Could not load records.");
    }
  }

  useEffect(() => {
    loadRecords();
  }, []);

  async function submit(event) {
    event.preventDefault();
    setStatus("");
    try {
      await createTestRecord(message);
      setStatus("Record saved successfully in MongoDB.");
      await loadRecords();
    } catch (err) {
      setStatus(err?.response?.data?.detail || "Could not save record.");
    }
  }

  return (
    <div className="mx-auto max-w-4xl">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">Phase 1 System Test</h1>
        <p className="mt-2 text-sm text-slate-500">
          This is a real database test, not fake demo data.
        </p>

        <form onSubmit={submit} className="mt-6 flex flex-col gap-3 sm:flex-row">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="flex-1 rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-emerald-500"
          />
          <button className="rounded-xl bg-emerald-600 px-5 py-3 font-semibold text-white hover:bg-emerald-700">
            Save Test Record
          </button>
        </form>

        {status && (
          <div className="mt-4 rounded-xl bg-slate-50 p-4 text-sm text-slate-700">{status}</div>
        )}

        <div className="mt-8">
          <h2 className="font-semibold text-slate-900">Saved records</h2>
          <div className="mt-3 space-y-2">
            {records.length === 0 ? (
              <p className="text-sm text-slate-400">No records yet.</p>
            ) : (
              records.map((record) => (
                <div key={record.id} className="rounded-xl border border-slate-100 p-4">
                  <p className="font-medium text-slate-800">{record.message}</p>
                  <p className="mt-1 text-xs text-slate-400">{new Date(record.created_at).toLocaleString()}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
