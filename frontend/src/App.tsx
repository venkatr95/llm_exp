import { useState, useEffect } from 'react'
import './App.css'
import UUIDComboBox from './components/UUIDComboBox'
import FormFields from './components/FormFields'
import { fetchFormData, fetchUUIDs } from './api/formApi'
import { FormData } from './types/FormData'

function App() {
    const [uuids, setUuids] = useState<string[]>([])
    const [selectedUUID, setSelectedUUID] = useState<string>('')
    const [formData, setFormData] = useState<FormData>({
        uuid: '',
        name: '',
        email: '',
        phone: '',
        address: '',
        company: '',
        position: '',
        notes: ''
    })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    // Load available UUIDs on mount
    useEffect(() => {
        loadUUIDs()
    }, [])

    const loadUUIDs = async () => {
        try {
            const data = await fetchUUIDs()
            setUuids(data)
        } catch (err) {
            setError('Failed to load UUIDs')
            console.error(err)
        }
    }

    const handleUUIDSelect = async (uuid: string) => {
        setSelectedUUID(uuid)
        setError(null)

        if (!uuid) {
            // Clear form if no UUID selected
            setFormData({
                uuid: '',
                name: '',
                email: '',
                phone: '',
                address: '',
                company: '',
                position: '',
                notes: ''
            })
            return
        }

        setLoading(true)

        try {
            const data = await fetchFormData(uuid)
            setFormData(data)
        } catch (err) {
            setError('Failed to fetch form data. Please check if the UUID exists.')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="app-container">
            <header className="app-header">
                <h1>🔐 UUID Form Filler</h1>
                <p className="subtitle">AI-powered form filling using OpenAI</p>
            </header>

            <main className="main-content">
                <div className="form-container">
                    <UUIDComboBox
                        uuids={uuids}
                        selectedUUID={selectedUUID}
                        onUUIDSelect={handleUUIDSelect}
                    />

                    {error && (
                        <div className="error-message">
                            ⚠️ {error}
                        </div>
                    )}

                    {loading && (
                        <div className="loading-message">
                            ⏳ Loading form data...
                        </div>
                    )}

                    <FormFields formData={formData} />
                </div>
            </main>

            <footer className="app-footer">
                <p>Powered by OpenAI GPT & FastAPI</p>
            </footer>
        </div>
    )
}

export default App
