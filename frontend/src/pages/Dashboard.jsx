import { useEffect, useState } from "react";
import StatusCard from "../components/StatusCard";
import { getApiHealth, getDatabaseHealth } from "../services/api";

export default function Dashboard() {
  const [apiStatus, setApiStatus] = useState("loading");
  const [dbStatus, setDbStatus] = useState("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    async function check() {
      try {
        const [api, db] = await Promise.all([getApiHealth(), getDatabaseHealth()]);
        setApiStatus(api.status === "ok" ? "connected" : "error");
        setDbStatus(db.connected ? "connected" : "error");
      } catch (err) {
        setApiStatus("error");
        setDbStatus("error");
        setError(err?.response?.data?.detail || "Could not reach the backend.");
      }
    }
    check();
  }, []);

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-8">
        <p className="text-sm font-semibold uppercase tracking-wider text-emerald-600">LactoVision</p>
        <h1 className="mt-1 text-3xl font-bold text-slate-900">Farm Dashboard</h1>
        <p className="mt-2 max-w-2xl text-slate-500">
          Phase 3 data layer: cattle, milk, feed, health and environmental records are connected to FastAPI and MongoDB. AI/ML begins in Phase 4.
        </p>
      </div>

      {error && (
        <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        <StatusCard
          title="Backend API"
          status={apiStatus}
          detail="FastAPI /api/health"
        />
        <StatusCard
          title="MongoDB"
          status={dbStatus}
          detail="FastAPI → MongoDB connection"
        />
      </div>

      <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">Current project scope</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {[
            "Authentication + JWT",
            "Farm management",
            "Cattle management",
            "Milk production records",
            "Feed & nutrition records",
            "Health + environment records",
          ].map((item) => (
            <div key={item} className="rounded-xl bg-slate-50 p-4 text-sm text-slate-700">
              ✓ {item}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
