import { FormData } from '../types/FormData';

interface FormFieldsProps {
    formData: FormData;
}

function FormFields({ formData }: FormFieldsProps) {
    return (
        <div className="form-fields">
            <div className="form-group">
                <label htmlFor="name">Name</label>
                <input
                    id="name"
                    type="text"
                    value={formData.name}
                    readOnly
                    placeholder="Name will appear here..."
                />
            </div>

            <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                    id="email"
                    type="email"
                    value={formData.email}
                    readOnly
                    placeholder="Email will appear here..."
                />
            </div>

            <div className="form-group">
                <label htmlFor="phone">Phone</label>
                <input
                    id="phone"
                    type="tel"
                    value={formData.phone}
                    readOnly
                    placeholder="Phone will appear here..."
                />
            </div>

            <div className="form-group">
                <label htmlFor="address">Address</label>
                <input
                    id="address"
                    type="text"
                    value={formData.address}
                    readOnly
                    placeholder="Address will appear here..."
                />
            </div>

            <div className="form-group">
                <label htmlFor="company">Company</label>
                <input
                    id="company"
                    type="text"
                    value={formData.company}
                    readOnly
                    placeholder="Company will appear here..."
                />
            </div>

            <div className="form-group">
                <label htmlFor="position">Position</label>
                <input
                    id="position"
                    type="text"
                    value={formData.position}
                    readOnly
                    placeholder="Position will appear here..."
                />
            </div>

            <div className="form-group">
                <label htmlFor="notes">Notes</label>
                <textarea
                    id="notes"
                    value={formData.notes}
                    readOnly
                    placeholder="Notes will appear here..."
                />
            </div>
        </div>
    );
}

export default FormFields;
