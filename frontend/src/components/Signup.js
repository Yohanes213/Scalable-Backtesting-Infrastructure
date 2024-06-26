import React from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { Link } from 'react-router-dom';
import axios from 'axios';
import qs from 'qs'
const validationSchema = Yup.object({
  username: Yup.string()
    .min(3, 'Username must be at least 3 characters')
    .required('Required'),
  password: Yup.string()
    .min(6, 'Password must be at least 6 characters')
    .matches(/[a-zA-Z]/, 'Password must contain a letter')
    // .matches(/\d/, 'Password must contain a number')
    // .matches(/[!@#$%^&*(),.?":{}|<>]/, 'Password must contain a special character')
    .required('Required'),
});

function Signup() {
  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
    },
    validationSchema,
    onSubmit: async (values) => {
      
      try {
        const response = await axios.post(
          'http://localhost:8000/auth/signup', 
          qs.stringify(values), 
          { headers: { 'Content-Type': 'application/json' } }

        );
        console.log('Signup successful!', response.data);

        alert('Signup successful! Please login to continue.');
        window.location.href = '/login'; 
      } catch (error) {
        console.error('Signup error:', error);
        const errorMessage = document.getElementById('error-message');
        if (errorMessage) {
          errorMessage.textContent = 'Signup failed. Please try again.';
        }
      }
    },
  });

  return (
    <div className="card bg-base-100 shadow-xl max-w-screen-sm">
      <div className="card-body">
        <h2 className="card-title">Sign Up</h2>
        <form onSubmit={formik.handleSubmit}>
          <div className="form-control">
            <label className="label">
              <span className="label-text">Username</span>
            </label>
            <input
              type="text"
              name="username"
              value={formik.values.username}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              className="input input-bordered"
              required
            />
            {formik.touched.username && formik.errors.username ? (
              <div className="text-red-500 text-sm">{formik.errors.username}</div>
            ) : null}
          </div>
          <div className="form-control">
            <label className="label">
              <span className="label-text">Password</span>
            </label>
            <input
              type="password"
              name="password"
              value={formik.values.password}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              className="input input-bordered"
              required
            />
            {formik.touched.password && formik.errors.password ? (
              <div className="text-red-500 text-sm">{formik.errors.password}</div>
            ) : null}
          </div>
          <div className="form-control mt-4">
            <button type="submit" className="btn btn-primary">
              Sign Up
            </button>
          </div>
        </form>
        <div className="mt-4">
          <p>Already have an account? <Link to="/login" className="text-blue-500">Login here</Link></p>
        </div>
        <div id="error-message"></div> {/* Added element for error message */}
      </div>
    </div>
  );
}

export default Signup;
