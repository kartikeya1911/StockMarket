"""
Portfolio Management Module
Handles portfolio tracking, management, and analysis
"""

import pandas as pd
import numpy as np
import streamlit as st
import os
from datetime import datetime
import config
from utils.stock_data import StockDataFetcher, format_currency

class PortfolioManager:
    """
    Class to manage stock portfolio
    """
    
    def __init__(self, portfolio_file=None):
        """
        Initialize Portfolio Manager
        
        Args:
            portfolio_file (str): Path to portfolio CSV file
        """
        self.portfolio_file = portfolio_file or config.PORTFOLIO_FILE
        self.portfolio = None
        self._ensure_file_exists()
        self.load_portfolio()
    
    def _ensure_file_exists(self):
        """
        Ensure portfolio file and directory exist
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.portfolio_file), exist_ok=True)
            
            # Create file if it doesn't exist
            if not os.path.exists(self.portfolio_file):
                # Create empty portfolio with headers
                empty_portfolio = pd.DataFrame(columns=[
                    'Ticker', 'Company_Name', 'Quantity', 'Purchase_Price',
                    'Purchase_Date', 'Total_Investment'
                ])
                empty_portfolio.to_csv(self.portfolio_file, index=False)
        
        except Exception as e:
            st.error(f"Error creating portfolio file: {str(e)}")
    
    def load_portfolio(self):
        """
        Load portfolio from CSV file
        
        Returns:
            pd.DataFrame: Portfolio data
        """
        try:
            self.portfolio = pd.read_csv(self.portfolio_file)
            return self.portfolio
        
        except Exception as e:
            st.error(f"Error loading portfolio: {str(e)}")
            return None
    
    def save_portfolio(self):
        """
        Save portfolio to CSV file
        
        Returns:
            bool: True if successful
        """
        try:
            if self.portfolio is not None:
                self.portfolio.to_csv(self.portfolio_file, index=False)
                return True
            return False
        
        except Exception as e:
            st.error(f"Error saving portfolio: {str(e)}")
            return False
    
    def add_stock(self, ticker, quantity, purchase_price, purchase_date=None):
        """
        Add a stock to the portfolio
        
        Args:
            ticker (str): Stock ticker symbol
            quantity (float): Number of shares
            purchase_price (float): Price per share at purchase
            purchase_date (str): Date of purchase (optional)
        
        Returns:
            bool: True if successful
        """
        try:
            # Get company name
            fetcher = StockDataFetcher(ticker)
            if not fetcher.validate_ticker():
                st.error(f"Invalid ticker: {ticker}")
                return False
            
            stock_info = fetcher.get_stock_info()
            company_name = stock_info['name'] if stock_info else ticker
            
            # Set purchase date
            if purchase_date is None:
                purchase_date = datetime.now().strftime('%Y-%m-%d')
            
            # Calculate total investment
            total_investment = quantity * purchase_price
            
            # Create new entry
            new_entry = pd.DataFrame({
                'Ticker': [ticker.upper()],
                'Company_Name': [company_name],
                'Quantity': [quantity],
                'Purchase_Price': [purchase_price],
                'Purchase_Date': [purchase_date],
                'Total_Investment': [total_investment]
            })
            
            # Add to portfolio
            self.portfolio = pd.concat([self.portfolio, new_entry], ignore_index=True)
            
            # Save to file
            return self.save_portfolio()
        
        except Exception as e:
            st.error(f"Error adding stock to portfolio: {str(e)}")
            return False
    
    def remove_stock(self, index):
        """
        Remove a stock from the portfolio by index
        
        Args:
            index (int): Index of the stock to remove
        
        Returns:
            bool: True if successful
        """
        try:
            if index < 0 or index >= len(self.portfolio):
                st.error("Invalid index")
                return False
            
            self.portfolio = self.portfolio.drop(index).reset_index(drop=True)
            return self.save_portfolio()
        
        except Exception as e:
            st.error(f"Error removing stock: {str(e)}")
            return False
    
    def update_stock(self, index, quantity=None, purchase_price=None):
        """
        Update stock information
        
        Args:
            index (int): Index of the stock to update
            quantity (float): New quantity (optional)
            purchase_price (float): New purchase price (optional)
        
        Returns:
            bool: True if successful
        """
        try:
            if index < 0 or index >= len(self.portfolio):
                st.error("Invalid index")
                return False
            
            if quantity is not None:
                self.portfolio.at[index, 'Quantity'] = quantity
            
            if purchase_price is not None:
                self.portfolio.at[index, 'Purchase_Price'] = purchase_price
            
            # Recalculate total investment
            self.portfolio.at[index, 'Total_Investment'] = (
                self.portfolio.at[index, 'Quantity'] * 
                self.portfolio.at[index, 'Purchase_Price']
            )
            
            return self.save_portfolio()
        
        except Exception as e:
            st.error(f"Error updating stock: {str(e)}")
            return False
    
    def get_portfolio_summary(self):
        """
        Get comprehensive portfolio summary with current values
        
        Returns:
            dict: Portfolio summary with metrics
        """
        try:
            if self.portfolio is None or self.portfolio.empty:
                return {
                    'total_stocks': 0,
                    'total_investment': 0,
                    'current_value': 0,
                    'total_gain_loss': 0,
                    'total_gain_loss_percent': 0,
                    'portfolio_details': None
                }
            
            # Get current prices for all stocks
            portfolio_details = []
            total_investment = 0
            total_current_value = 0
            
            for idx, row in self.portfolio.iterrows():
                ticker = row['Ticker']
                fetcher = StockDataFetcher(ticker)
                
                # Get current price
                price_info = fetcher.get_realtime_price()
                current_price = price_info['current_price'] if price_info else 0
                
                # Calculate metrics
                quantity = row['Quantity']
                purchase_price = row['Purchase_Price']
                investment = row['Total_Investment']
                current_value = quantity * current_price
                gain_loss = current_value - investment
                gain_loss_percent = (gain_loss / investment * 100) if investment > 0 else 0
                
                total_investment += investment
                total_current_value += current_value
                
                portfolio_details.append({
                    'Ticker': ticker,
                    'Company_Name': row['Company_Name'],
                    'Quantity': quantity,
                    'Purchase_Price': purchase_price,
                    'Current_Price': current_price,
                    'Purchase_Date': row['Purchase_Date'],
                    'Investment': investment,
                    'Current_Value': current_value,
                    'Gain_Loss': gain_loss,
                    'Gain_Loss_Percent': gain_loss_percent
                })
            
            # Calculate overall metrics
            total_gain_loss = total_current_value - total_investment
            total_gain_loss_percent = (
                (total_gain_loss / total_investment * 100) 
                if total_investment > 0 else 0
            )
            
            return {
                'total_stocks': len(self.portfolio),
                'total_investment': total_investment,
                'current_value': total_current_value,
                'total_gain_loss': total_gain_loss,
                'total_gain_loss_percent': total_gain_loss_percent,
                'portfolio_details': pd.DataFrame(portfolio_details)
            }
        
        except Exception as e:
            st.error(f"Error calculating portfolio summary: {str(e)}")
            return None
    
    def get_portfolio_allocation(self):
        """
        Get portfolio allocation by stock
        
        Returns:
            pd.DataFrame: Allocation data
        """
        try:
            summary = self.get_portfolio_summary()
            if summary is None or summary['portfolio_details'] is None:
                return None
            
            details = summary['portfolio_details']
            total_value = summary['current_value']
            
            # Calculate allocation percentage
            details['Allocation_Percent'] = (
                details['Current_Value'] / total_value * 100
            ) if total_value > 0 else 0
            
            return details[['Ticker', 'Company_Name', 'Current_Value', 'Allocation_Percent']]
        
        except Exception as e:
            st.error(f"Error calculating allocation: {str(e)}")
            return None
    
    def get_best_worst_performers(self):
        """
        Get best and worst performing stocks
        
        Returns:
            dict: Best and worst performers
        """
        try:
            summary = self.get_portfolio_summary()
            if summary is None or summary['portfolio_details'] is None:
                return None
            
            details = summary['portfolio_details']
            
            if details.empty:
                return None
            
            # Sort by gain/loss percentage
            sorted_details = details.sort_values('Gain_Loss_Percent', ascending=False)
            
            best_performer = sorted_details.iloc[0]
            worst_performer = sorted_details.iloc[-1]
            
            return {
                'best': {
                    'ticker': best_performer['Ticker'],
                    'company': best_performer['Company_Name'],
                    'gain_loss_percent': best_performer['Gain_Loss_Percent'],
                    'gain_loss': best_performer['Gain_Loss']
                },
                'worst': {
                    'ticker': worst_performer['Ticker'],
                    'company': worst_performer['Company_Name'],
                    'gain_loss_percent': worst_performer['Gain_Loss_Percent'],
                    'gain_loss': worst_performer['Gain_Loss']
                }
            }
        
        except Exception as e:
            return None
    
    def clear_portfolio(self):
        """
        Clear all stocks from portfolio
        
        Returns:
            bool: True if successful
        """
        try:
            self.portfolio = pd.DataFrame(columns=[
                'Ticker', 'Company_Name', 'Quantity', 'Purchase_Price',
                'Purchase_Date', 'Total_Investment'
            ])
            return self.save_portfolio()
        
        except Exception as e:
            st.error(f"Error clearing portfolio: {str(e)}")
            return False


# ==================== HELPER FUNCTIONS ====================

def calculate_portfolio_metrics(portfolio_summary):
    """
    Calculate advanced portfolio metrics
    
    Args:
        portfolio_summary (dict): Portfolio summary data
    
    Returns:
        dict: Advanced metrics
    """
    try:
        if portfolio_summary is None or portfolio_summary['portfolio_details'] is None:
            return None
        
        details = portfolio_summary['portfolio_details']
        
        # Calculate diversification metrics
        num_stocks = len(details)
        
        # Calculate weighted average gain/loss
        total_value = portfolio_summary['current_value']
        if total_value > 0:
            weighted_gain = sum(
                details['Gain_Loss_Percent'] * details['Current_Value']
            ) / total_value
        else:
            weighted_gain = 0
        
        # Risk assessment (based on allocation concentration)
        max_allocation = details['Current_Value'].max() / total_value * 100 if total_value > 0 else 0
        
        if max_allocation > 40:
            risk_level = "High - Portfolio is concentrated"
        elif max_allocation > 25:
            risk_level = "Moderate - Consider more diversification"
        else:
            risk_level = "Low - Well diversified"
        
        return {
            'num_stocks': num_stocks,
            'weighted_avg_gain': weighted_gain,
            'max_allocation_percent': max_allocation,
            'risk_level': risk_level
        }
    
    except Exception as e:
        return None


def export_portfolio_report(portfolio_summary, filename='portfolio_report.csv'):
    """
    Export portfolio details to CSV
    
    Args:
        portfolio_summary (dict): Portfolio summary
        filename (str): Output filename
    
    Returns:
        bool: True if successful
    """
    try:
        if portfolio_summary is None or portfolio_summary['portfolio_details'] is None:
            return False
        
        details = portfolio_summary['portfolio_details']
        details.to_csv(filename, index=False)
        return True
    
    except Exception as e:
        st.error(f"Error exporting report: {str(e)}")
        return False
