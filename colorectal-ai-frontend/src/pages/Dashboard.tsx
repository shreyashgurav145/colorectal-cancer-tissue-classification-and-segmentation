```tsx
import { Activity, Plus, ScanLine, UsersRound } from "lucide-react";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../services/api";

type Patient = {
  id: number;
  patient_id: string;
  name: string;
  age: number;
  gender: string;
  created_at: string;
};

export function Dashboard() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadPatients() {
      try {
        const response = await api.get("/patients");
        setPatients(response.data);
      } catch {
        setError("Unable to load patients.");
      } finally {
        setLoading(false);
      }
    }

    loadPatients();
  }, []);

  return (
    <section className="section">
      <p className="eyebrow">USER DASHBOARD</p>

      <h1>Welcome, Researcher</h1>

      {error && <p className="error">{error}</p>}

      <div className="stat-grid">
        <div>
          <UsersRound />
          <b>{loading ? "..." : patients.length}</b>
          <span>Total patients</span>
        </div>

        <div>
          <Activity />
          <b>—</b>
          <span>Total predictions</span>
        </div>

        <div>
          <ScanLine />
          <b>—</b>
          <span>Recent analysis</span>
        </div>
      </div>

      <Link className="button" to="/patients/new">
        <Plus size={18} />
        Add patient
      </Link>

      <div className="panel" style={{ marginTop: "2rem" }}>
        <h2>Recent Patients</h2>

        {loading ? (
          <p>Loading patients...</p>
        ) : patients.length === 0 ? (
          <p>No patients added yet.</p>
        ) : (
          <div>
            {patients.map((patient) => (
              <div key={patient.id}>
                <strong>{patient.name}</strong>
                <p>
                  Patient ID: {patient.patient_id} | Age: {patient.age} |{" "}
                  {patient.gender}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
```
