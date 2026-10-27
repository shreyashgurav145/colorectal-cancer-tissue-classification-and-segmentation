import type { FormEvent } from "react";
import { useState } from "react";
import { UploadCloud } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";

type PredictionResult = {
  id: number;
  predicted_class: string;
  confidence: number;
  probabilities: number[];
  mask_path: string;
  overlay_path: string;
};

export function AddPatient() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();

    setMessage("");
    setError("");

    if (!file) {
      setError("Please select a testing image.");
      return;
    }

    const form = new FormData(e.currentTarget);

    try {
      setLoading(true);

      const patientResponse = await api.post("/patients", {
        patient_id: form.get("patient_id"),
        name: form.get("name"),
        address: form.get("address"),
        age: Number(form.get("age")),
        gender: form.get("gender"),
        contact: form.get("contact"),
      });

      const patient = patientResponse.data;

      const predictionData = new FormData();
      predictionData.append("patient_id", String(patient.id));
      predictionData.append("image", file);

      const predictionResponse = await api.post<PredictionResult>(
        "/prediction",
        predictionData
      );

      const prediction = predictionResponse.data;

      const confidence = (prediction.confidence * 100).toFixed(2);

      setMessage(
        "Analysis completed: " +
          prediction.predicted_class +
          " (" +
          confidence +
          "%)"
      );

      setTimeout(() => {
        navigate("/patients/" + patient.id + "/results", {
          state: {
            patient: patient,
            prediction: prediction,
          },
        });
      }, 800);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          "Unable to save patient or complete AI analysis."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="section narrow">
      <p className="eyebrow">PATIENT INTAKE</p>

      <h1>Add patient and test image</h1>

      {message && <p className="notice">{message}</p>}

      {error && <p className="error">{error}</p>}

      <form className="form panel" onSubmit={submit}>
        <div className="two-columns">
          <label>
            Patient ID
            <input name="patient_id" required />
          </label>

          <label>
            Patient name
            <input name="name" required />
          </label>

          <label>
            Age
            <input name="age" type="number" min="0" required />
          </label>

          <label>
            Gender
            <select name="gender" required>
              <option value="">Select</option>
              <option value="Female">Female</option>
              <option value="Male">Male</option>
              <option value="Other">Other</option>
            </select>
          </label>
        </div>

        <label>
          Address
          <textarea name="address" required rows={3} />
        </label>

        <label>
          Contact number
          <input name="contact" required />
        </label>

        <label className="dropzone">
          <UploadCloud />

          <span>
            {file
              ? file.name
              : "Choose a JPG, JPEG, or PNG testing image"}
          </span>

          <input
            type="file"
            accept=".jpg,.jpeg,.png,image/jpeg,image/png"
            onChange={(e) => {
              setFile(e.target.files?.[0] ?? null);
            }}
            required
          />
        </label>

        <button
          className="button"
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Saving patient and running AI..."
            : "Save patient and run AI analysis"}
        </button>
      </form>
    </section>
  );
}
