import { useEffect, useState } from "react";
import { getCows, getPredictionFields, predictYield, getPredictions } from "../services/api";

export default function Prediction() {
  const [cows, setCows] = useState([]);
  const [fields, setFields] = useState([]);
  const [numeric, setNumeric] = useState([]);
  const [cowId, setCowId] = useState("");
  const [inputs, setInputs] = useState({});
  const [history, setHistory] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const refresh = () => getPredictions().then(setHistory).catch(() => {});
  useEffect(() => {
    getCows().then(setCows).catch(e => setError(e.response?.data?.detail || e.message));
    getPredictionFields().then(d => {setFields(d.features); setNumeric(d.numerical_features);}).catch(e => setError(e.message));
    refresh();
  }, []);
  const selected = cows.find(c => c.id === cowId);
  useEffect(() => {
    if (!selected) return;
    setInputs(p => ({...p, breed:selected.breed, age_years:selected.age,
      body_weight_kg:selected.weight, parity:selected.parity,
      lactation_stage:selected.lactation_stage, health_status:selected.health_status}));
  }, [cowId]);
  const submit = async e => {
    e.preventDefault(); setError(""); setResult(null); setBusy(true);
    try {const r = await predictYield({cow_id:cowId, inputs}); setResult(r); await refresh();}
    catch(e) {setError(e.response?.data?.detail || e.message);}
    finally {setBusy(false);}
  };
  return <div className="mx-auto max-w-6xl space-y-6">
    <h1 className="text-3xl font-bold text-slate-900">Milk Yield Prediction</h1>
    <p className="text-slate-600">Random Forest model trained on synthetic data. Enter measured inputs; leave unavailable fields blank. This is decision support, not a veterinary diagnosis.</p>
    {error && <p role="alert" className="rounded-lg bg-red-50 p-4 text-red-700">{String(error)}</p>}
    <form onSubmit={submit} className="rounded-xl bg-white p-6 shadow-sm space-y-5">
      <label className="block font-medium">Cow
        <select required value={cowId} onChange={e=>setCowId(e.target.value)} className="mt-1 block w-full rounded-lg border p-2">
          <option value="">Select a registered cow</option>{cows.map(c=><option key={c.id} value={c.id}>{c.name} ({c.cow_id})</option>)}
        </select>
      </label>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{fields.map(f => <label key={f} className="text-sm font-medium text-slate-700">{f.replaceAll("_", " ")}
        <input className="mt-1 block w-full rounded-lg border p-2" type={numeric.includes(f)?"number":"text"} step="any" value={inputs[f]??""}
          onChange={e=>setInputs(p=>({...p,[f]:e.target.value===""?undefined:numeric.includes(f)?Number(e.target.value):e.target.value}))} />
      </label>)}</div>
      <button disabled={busy || !cowId} className="rounded-lg bg-emerald-700 px-5 py-3 font-semibold text-white disabled:opacity-50">{busy?"Predicting...":"Predict and save"}</button>
    </form>
    {result && <section className="rounded-xl border border-emerald-200 bg-emerald-50 p-6 space-y-2">
      <h2 className="text-xl font-bold">Predicted yield: {result.predicted_milk_yield_kg.toFixed(2)} kg/day</h2>
      <p>Model: {result.model_used}</p>
      <h3 className="font-semibold">Recommendations</h3>{result.recommendations.map((x,i)=><p key={i}>{x}</p>)}
      {result.health_alerts.map((x,i)=><p className="text-amber-800" key={i}>{x}</p>)}
    </section>}
    <section className="rounded-xl bg-white p-6 shadow-sm"><h2 className="text-xl font-bold mb-3">Prediction history</h2>
      {!history.length && <p>No predictions saved yet.</p>}
      {history.map(h=><div key={h.id} className="border-t py-3">{new Date(h.created_at).toLocaleString()} — {h.predicted_milk_yield_kg.toFixed(2)} kg/day ({h.model_used})</div>)}
    </section>
  </div>;
}
