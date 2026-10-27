import { CheckCircle2, XCircle, LoaderCircle } from "lucide-react";

export default function StatusCard({ title, status, detail }) {
  const loading = status === "loading";
  const connected = status === "connected";

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">{title}</p>
        {loading ? (
          <LoaderCircle className="animate-spin text-slate-400" size={20} />
        ) : connected ? (
          <CheckCircle2 className="text-emerald-600" size={20} />
        ) : (
          <XCircle className="text-red-500" size={20} />
        )}
      </div>
      <p className="mt-2 text-lg font-semibold text-slate-900">
        {loading ? "Checking..." : connected ? "Connected" : "Not connected"}
      </p>
      <p className="mt-1 text-sm text-slate-500">{detail}</p>
    </div>
  );
}
