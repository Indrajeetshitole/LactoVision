import { useEffect, useState } from "react";
import { getCows } from "../services/api";

export default function CowSelector({ value, onChange, required = true }) {
  const [cows, setCows] = useState([]);
  const [error, setError] = useState("");
  useEffect(() => {
    getCows().then(setCows).catch((e) => setError(e?.response?.data?.detail || "Could not load cows."));
  }, []);
  return (
    <label className="block">
      <span className="text-sm font-medium text-slate-700">Cow</span>
      <select required={required} value={value} onChange={(e) => onChange(e.target.value)} className="mt-1 w-full rounded-xl border border-slate-300 bg-white px-4 py-3">
        <option value="">Select cow</option>
        {cows.map((cow) => <option key={cow.id} value={cow.id}>{cow.cow_id} — {cow.name} ({cow.breed})</option>)}
      </select>
      {error && <span className="mt-1 block text-xs text-red-600">{error}</span>}
    </label>
  );
}
