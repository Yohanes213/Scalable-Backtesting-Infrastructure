import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import BacktestForm from './BacktestForm';  

jest.mock('axios');

describe('BacktestForm Component', () => {
  test('renders backtest form', () => {
    render(<BacktestForm />);

    expect(screen.getByLabelText(/Start Date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/End Date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Coin Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Strategy/i)).toBeInTheDocument();
    expect(screen.getByText(/Run Backtest/i)).toBeInTheDocument();
  });

  test('handles successful backtest', async () => {
    axios.post.mockResolvedValueOnce({
      data: {
        return: "10%",
        numberOfTrades: 50,
        winningTrades: 30,
        losingTrades: 20,
        maxDrawdown: "5%",
        sharpeRatio: 1.5
      }
    });

    render(<BacktestForm />);

    // Fill out the form
    fireEvent.change(screen.getByLabelText(/Start Date/i), {
      target: { value: '2023-01-01' },
    });
    fireEvent.change(screen.getByLabelText(/End Date/i), {
      target: { value: '2023-12-31' },
    });
    fireEvent.change(screen.getByLabelText(/Coin Name/i), {
      target: { value: 'Bitcoin' },
    });
    fireEvent.change(screen.getByLabelText(/Strategy/i), {
      target: { value: 'SMA' },
    });

    fireEvent.change(screen.getByLabelText(/Short Period/i), {
      target: { value: '5' },
    });
    fireEvent.change(screen.getByLabelText(/Long Period/i), {
      target: { value: '20' },
    });
    fireEvent.change(screen.getByLabelText(/Commission/i), {
      target: { value: '0.01' },
    });

    fireEvent.click(screen.getByText(/Run Backtest/i));

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:8000/scenes/backtest',
        {
          startDate: '2023-01-01',
          endDate: '2023-12-31',
          coinName: 'Bitcoin',
          strategy: 'SMA',
          params: {
            short_period: '5',
            long_period: '20',
            commission: '0.01'
          }
        }
      );
    });

 
  });

  test('handles backtest error', async () => {
    axios.post.mockRejectedValueOnce(new Error('Backtest failed'));

    render(<BacktestForm />);

    fireEvent.change(screen.getByLabelText(/Start Date/i), {
      target: { value: '2023-01-01' },
    });
    fireEvent.change(screen.getByLabelText(/End Date/i), {
      target: { value: '2023-12-31' },
    });
    fireEvent.change(screen.getByLabelText(/Coin Name/i), {
      target: { value: 'Bitcoin' },
    });
    fireEvent.change(screen.getByLabelText(/Strategy/i), {
      target: { value: 'SMA' },
    });

    fireEvent.change(screen.getByLabelText(/Short Period/i), {
      target: { value: '5' },
    });
    fireEvent.change(screen.getByLabelText(/Long Period/i), {
      target: { value: '20' },
    });
    fireEvent.change(screen.getByLabelText(/Commission/i), {
      target: { value: '0.01' },
    });

    fireEvent.click(screen.getByText(/Run Backtest/i));

    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:8000/scenes/backtest',
        {
          startDate: '2023-01-01',
          endDate: '2023-12-31',
          coinName: 'Bitcoin',
          strategy: 'SMA',
          params: {
            short_period: '5',
            long_period: '20',
            commission: '0.01'
          }
        }
      );
    });

    await waitFor(() => {
      const errorMessage = screen.getByText(/Backtest failed. Please try again./i);
      expect(errorMessage).toBeInTheDocument();
    });
  });
});
