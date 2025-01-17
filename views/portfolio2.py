import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np
from datetime import timedelta
import datetime as dt

st.header('Sales Dashboard 📊')


# --- Function Defs ---
def format_large_number(value):  # Format large numbers
    if isinstance(value, int):  # Check if the value is an integer
        if value >= 1_000_000:
            return f"{value // 1_000_000}M"
        elif value >= 1_000:
            return f"{value // 1_000}K"
        else:
            return f"{value:,}"  # No decimal places for small integers
    elif isinstance(value, float):  # For floats
        if value >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"
        elif value >= 1_000:
            return f"{value / 1_000:.2f}K"
        else:
            return f"{value:,.2f}"  # Two decimal places for small floats
    else:
        raise ValueError("Input must be an int or float.")


# --- Import & Clean Data ---
sales_df = pd.read_csv(r'./assets/salesDF.csv')
sales_df = sales_df.drop(sales_df.columns[0], axis=1)
# Convert the 'Order Received' and 'Order Delivered' columns directly to datetime
sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
sales_df['start_ship_date'] = pd.to_datetime(sales_df['start_ship_date'])
# Convert Line Item Total to numeric, strip formatting
sales_df['line_item_total'] = sales_df['line_item_total'].replace('[\\$,]', '', regex=True)
sales_df['line_item_total'] = pd.to_numeric(sales_df['line_item_total'])
# Remove anomalies
sales_df = sales_df[~sales_df['anon_category'].isin(['Category_4', 'Category_5', 'Category_6'])]
# Rename and Reorder Columns
column_names = {
    'orderID': 'Order #',
    'anon_customer': 'Customer',
    'order_date': 'Order Received',
    'start_ship_date': 'Order Delivered',
    'anon_rep': 'Sales Rep',
    'anon_product_line': 'Product Line',
    'anon_product': 'Product',
    'line_item_total': 'Line Item Total ($)',
    'anon_category': 'Product Category'
}
sales_df = sales_df.rename(columns=column_names)
col_order = ['Order #', 'Customer', 'Sales Rep', 'Order Received', 'Order Delivered', 'Product Category', 'Product Line', 'Product', 'Qty (Units)', 'Line Item Total ($)']
sales_df = sales_df[col_order]


# --- Set Filters ---
st.subheader('Filters')
cola, colb, colc, cold = st.columns(4)
with cola:
    reps = st.multiselect('Sales Representative', sales_df['Sales Rep'].unique(), placeholder='Select Sales Rep(s)')
with colc:
    lines = st.multiselect('Product Line', sales_df['Product Line'].unique(), placeholder='Select Product Line(s)')
with colb:
    cats = st.multiselect('Product Category', sales_df['Product Category'].unique(), placeholder='Select Categories')
with cold:
    cust = st.multiselect('Customer', sales_df['Customer'].unique(), placeholder='Select customer(s)')
# Date Range Filters
with cola:
    min_date = sales_df['Order Received'].min()  # Get the minimum date from the 'Order Received' column
    max_date = dt.datetime.today()  # Get the maximum date from the 'Order Received' column
    start_date = st.date_input('Start Date', min_value=min_date, max_value=max_date, value=min_date)
with colb:
    end_date = st.date_input('End Date', min_value=min_date, max_value=max_date, value=max_date)


# --- Apply Filters ---
filtered = sales_df.copy()
if reps:
    filtered = filtered[filtered['Sales Rep'].isin(reps)]
if cats:
    filtered = filtered[filtered['Product Category'].isin(cats)]
if lines:
    filtered = filtered[filtered['Product Line'].isin(lines)]
if cust:
    filtered = filtered[filtered['Customer'].isin(cust)]

# Apply the date range filter to the 'Order Received' column
filtered = filtered[(filtered['Order Received'] >= pd.to_datetime(start_date)) & 
                     (filtered['Order Received'] <= pd.to_datetime(end_date))]


# --- Dashboard ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Sales Trends', 'Sales Reps', 'Product Analysis', 'Customers', 'Turnaround Time'])
# 1) Sales Trends
with tab1:
    col1, col2 = st.columns([2, 2])
    with col1:
        # 'Order Received' and 'Order Delivered' are already datetime, no need to convert them again
        # Group by 'Order ID' and calculate the total for each order
        sales_summary = filtered.groupby('Order #')['Line Item Total ($)'].sum().reset_index()

        # Calculate the total sales for all orders in the filtered DataFrame
        total_sales = sales_summary['Line Item Total ($)'].sum()

        # Format the total sales with shorthand notation
        formatted_total_sales = format_large_number(total_sales)

        # Display the total sales using st.metric (formatted with shorthand notation)
        st.metric(label='Total Sales', value=f"${formatted_total_sales}")        
    with col2:
        # --- Sales Over Time Trend Chart ---
        # Check if the date range is less than 91 days
        date_range = filtered['Order Received'].max() - filtered['Order Received'].min()        
        # If the time range is less than 91 days, group by week, else group by month
        if date_range < timedelta(days=91):
            filtered['Week'] = filtered['Order Received'].dt.to_period('W')
            time_period_col = 'Week'
        else:
            filtered['Year-Month'] = filtered['Order Received'].dt.to_period('M')
            time_period_col = 'Year-Month'
        # Aggregate sales by the chosen time period (week or month)
        sales_by_period = filtered.groupby(time_period_col)['Line Item Total ($)'].sum().reset_index()
        # Ensure the time period column is a proper datetime type for sorting
        sales_by_period[time_period_col] = sales_by_period[time_period_col].dt.to_timestamp()
        # Extract x and y values for regression
        x = np.arange(len(sales_by_period))  # Numeric index for time periods
        y = sales_by_period['Line Item Total ($)'].values
        # Error handling for insufficient or invalid data
        if len(x) < 2:
            st.error("Insufficient data to generate a trendline. At least two data points are required.")
        else:
            try:
                # Filter out invalid values
                valid_mask = np.isfinite(x) & np.isfinite(y)
                x = x[valid_mask]
                y = y[valid_mask]
                # Ensure there are still enough data points after filtering
                if len(x) < 2:
                    raise ValueError("Filtered data contains fewer than two valid points.")
                # Calculate linear regression for the trend line
                coefficients = np.polyfit(x, y, 1)  # 1st-degree polynomial (linear)
                trend = np.poly1d(coefficients)  # Trend line equation
                trend_line = trend(x)
                # Refined Plot using Matplotlib
                fig, ax = plt.subplots(figsize=(8, 4))                
                # Plot the sales data
                ax.plot(
                    sales_by_period[time_period_col], 
                    sales_by_period['Line Item Total ($)'], 
                    marker='o', 
                    color='#53A2BE', 
                    linestyle='-', 
                    linewidth=2
                )
                # Plot the trend line
                ax.plot(
                    sales_by_period[time_period_col], 
                    trend_line, 
                    color='#FF5733',  # Trend line color
                    linestyle='--', 
                    linewidth=2
                )                
                # Title and Labels
                ax.set_title('Sales Over Time', fontsize=14, weight='bold', color='#333333')
                # Format y-axis as currency
                ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
                # Rotate x-axis labels for readability
                ax.tick_params(axis='x', rotation=45)
                # Add a grid for better readability
                #ax.grid(visible=True, which='major', color='#CCCCCC', linestyle='--', linewidth=0.5)
                # Remove spines for a cleaner look
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                # Display the plot in Streamlit
                st.pyplot(fig, use_container_width=True)
            except np.linalg.LinAlgError:
                st.error("Trendline calculation failed due to numerical instability.")
            except ValueError as e:
                st.error(str(e))
# 2) Sales Reps
with tab2:
    col1, col2 = st.columns([2,2])
    # Aggregate orders by unique Order # to calculate total sales per order
    order_totals = filtered.groupby('Order #').agg(
        total_order_sales=('Line Item Total ($)', 'sum'),
        customer=('Customer', 'first'),
        sales_rep=('Sales Rep', 'first'),
        order_received=('Order Received', 'first')
    ).reset_index()
    # Calculate the total sales by sales rep
    sales_by_rep = order_totals.groupby('sales_rep')['total_order_sales'].sum().reset_index()
    # Find the top-selling rep (the one with the highest total sales)
    top_selling_rep = sales_by_rep.loc[sales_by_rep['total_order_sales'].idxmax()]
    # Calculate the average monthly sales per rep
    # Add a 'Year-Month' column to order_totals for monthly aggregation
    order_totals['Year-Month'] = order_totals['order_received'].dt.to_period('M')
    avg_monthly_sales = order_totals.groupby(['sales_rep', 'Year-Month'])['total_order_sales'].sum().reset_index()
    avg_monthly_sales = avg_monthly_sales.groupby('sales_rep')['total_order_sales'].mean().reset_index()
    # Calculate the biggest sale per rep
    biggest_sale = order_totals.groupby('sales_rep')['total_order_sales'].max().reset_index()
    # Merge these metrics together
    sales_rep_metrics = sales_by_rep.merge(avg_monthly_sales, on='sales_rep', suffixes=('_total', '_avg_monthly'))
    sales_rep_metrics = sales_rep_metrics.merge(biggest_sale, on='sales_rep')
    # Display metrics for the top-selling rep
    with col1:
        st.caption(f"Top Selling Rep")
        st.subheader(top_selling_rep['sales_rep'])
        # Format and display metrics using the format_large_number function
        total_sales = top_selling_rep['total_order_sales']
        avg_monthly_sales = sales_rep_metrics.loc[sales_rep_metrics['sales_rep'] == top_selling_rep['sales_rep'], 'total_order_sales_avg_monthly'].values[0]
        biggest_sale = sales_rep_metrics.loc[sales_rep_metrics['sales_rep'] == top_selling_rep['sales_rep'], 'total_order_sales'].max()
        st.metric(label="Total Sales", value=f"${format_large_number(total_sales)}")
        st.metric(label="Average Monthly Sales", value=f"${format_large_number(avg_monthly_sales)}")
        st.metric(label="Biggest Sale", value=f"${format_large_number(biggest_sale)}")
    with col2:
        # Show a bar chart of total sales by sales rep
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(sales_rep_metrics['sales_rep'], sales_rep_metrics['total_order_sales_total'], color='#53A2BE')
        # Title and formatting
        ax.set_title('Sales by Rep', fontsize=16, weight='bold')
        ax.set_xlabel('Sales Rep')
        ax.set_ylabel('Total Sales ($)')
        ax.tick_params(axis='x', rotation=45)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        #ax.grid(visible=True, which='major', color='#CCCCCC', linestyle='--', linewidth=0.5)
        # Remove spines for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig, use_container_width=True)

# 3) Sales Performance by Product Line and Product Category 
with tab3:    
    col1, col2 = st.columns([2, 2])    
    with col1:
        # Calculate Total Sales
        total_sales = filtered['Line Item Total ($)'].sum()
        # Top Product Category by Sales
        top_product_category = filtered.groupby('Product Category')['Line Item Total ($)'].sum().idxmax()
        top_product_category_sales = filtered.groupby('Product Category')['Line Item Total ($)'].sum().max()
        # Top Product Line by Sales
        top_product_line = filtered.groupby('Product Line')['Line Item Total ($)'].sum().idxmax()
        top_product_line_sales = filtered.groupby('Product Line')['Line Item Total ($)'].sum().max()
        # Number of Product Categories and Product Lines
        num_product_categories = filtered['Product Category'].nunique()
        num_product_lines = filtered['Product Line'].nunique()
        # Average Sales per Product Line
        avg_sales_per_product_line = filtered.groupby('Product Line')['Line Item Total ($)'].sum().mean()
        # Display Metrics with formatted values
        st.caption("Sales Metrics")
        st.metric(label="Total Sales", value=f"${format_large_number(total_sales)}")
        st.caption("Top Product Category by Sales")
        st.subheader(f"{top_product_category} (${format_large_number(top_product_category_sales)})")
        st.caption("Top Product Line by Sales")
        st.subheader(f"{top_product_line} (${format_large_number(top_product_line_sales)})")
        st.metric(label="Number of Product Categories", value=f"{format_large_number(num_product_categories)}")
        st.metric(label="Number of Product Lines", value=f"{format_large_number(num_product_lines)}")
        st.metric(label="Average Sales per Product Line", value=f"${format_large_number(avg_sales_per_product_line)}")
    with col2:        
        # Group by Product Category and Product Line, then sum Line Item Total ($)
        sales_by_product = filtered.groupby(['Product Category', 'Product Line'])['Line Item Total ($)'].sum().reset_index()
        # Pivot the data so that each Product Line becomes a separate column under each Product Category
        sales_pivot = sales_by_product.pivot(index='Product Category', columns='Product Line', values='Line Item Total ($)')
        # Plotting the stacked bar chart
        fig, ax = plt.subplots(figsize=(10, 6))        
        # Plot the stacked bar chart
        sales_pivot.plot(kind='bar', stacked=True, ax=ax, cmap='Set3', width=0.8)
        # Title and Labels
        ax.set_title('Sales Performance by Product Line per Category', fontsize=14, weight='bold', color='#333333')
        ax.setxlabel(None)
        #ax.set_ylabel('Line Item Total ($)', fontsize=12)
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        # Rotate x-axis labels for readability
        ax.tick_params(axis='x', rotation=45)
        # Add a grid for better readability
        #ax.grid(visible=False, which='major', color='#CCCCCC', linestyle='--', linewidth=0.5)
        # Remove spines for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Display the plot in Streamlit
        st.pyplot(fig, use_container_width=True)

# 4) Customers Panel 
with tab4:
    n = st.select_slider("Select number of top customers", options=range(1, 26), value=10)
    col1, col2 = st.columns([2, 2])
    # Aggregating customer-level data (calculations done before formatting)
    customer_sales_summary = filtered.groupby('Customer').agg(
        total_sales=('Line Item Total ($)', 'sum'),
        order_count=('Order #', 'nunique'),
        avg_order_value=('Line Item Total ($)', 'mean'),
        biggest_order=('Line Item Total ($)', 'max')
    ).reset_index()
    # Sort by 'total_sales' in descending order and limit to top n customers
    customer_sales_summary = customer_sales_summary.sort_values(by='total_sales', ascending=False).head(n)
    # Convert the 'total_sales', 'avg_order_value', and 'biggest_order' to numeric for plotting
    customer_sales_summary['total_sales_numeric'] = customer_sales_summary['total_sales']
    customer_sales_summary['avg_order_value_numeric'] = customer_sales_summary['avg_order_value']
    customer_sales_summary['biggest_order_numeric'] = customer_sales_summary['biggest_order']
    # Format large numbers only for display metrics
    customer_sales_summary['total_sales'] = customer_sales_summary['total_sales'].apply(format_large_number)
    customer_sales_summary['avg_order_value'] = customer_sales_summary['avg_order_value'].apply(format_large_number)
    customer_sales_summary['biggest_order'] = customer_sales_summary['biggest_order'].apply(format_large_number)    
    with col1:
        # --- Top Customer by Total Sales ---
        top_customer = customer_sales_summary.loc[customer_sales_summary['total_sales_numeric'].idxmax()]
        st.caption("Top Customer by Total Sales")
        st.subheader(top_customer['Customer'])
        st.metric(label="Total Sales", value='$'+top_customer['total_sales'])
        st.metric(label="Average Order Value", value='$'+top_customer['avg_order_value'])
        st.metric(label="Biggest Order", value='$'+top_customer['biggest_order'])
    with col2:
        cont = st.container(height=700, border=True)
        with cont:
            # --- Total Sales by Customer Bar Chart ---
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(customer_sales_summary['Customer'], customer_sales_summary['total_sales_numeric'], color='#53A2BE')
            ax.set_xlabel('Total Sales')
            
            # Remove spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)        
            st.pyplot(fig, use_container_width=True)
            # --- Number of Orders per Customer Bar Chart ---
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(customer_sales_summary['Customer'], customer_sales_summary['order_count'], color='#EF8354')
            ax.set_xlabel('Number of Orders')
                
            # Remove spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            st.pyplot(fig, use_container_width=True)

# 5) Turnaround Time 
with tab5:
    col1, col2 = st.columns([2,2])  
    # Calculate 'TAT (days)' as the difference in days (ensure no NaT values)
    filtered['TAT (days)'] = (filtered['Order Delivered'] - filtered['Order Received']).dt.days
    # Remove rows with negative or NaT 'TAT (days)'
    filtered = filtered[filtered['TAT (days)'] >= 0]
    # Optional: Drop rows with NaT values in 'TAT (days)' to avoid issues in plotting
    filtered = filtered.dropna(subset=['TAT (days)'])
    with col1:
        avg_tat = filtered['TAT (days)'].mean()
        st.metric(label='Avg Turnaround Time', value=f'{avg_tat:.0f} days')
    with col2:
        # Aggregate by 'Order #'
        aggregated = filtered.groupby('Order #')['TAT (days)'].max().reset_index()
        # Check if there's enough data to generate a histogram
        if aggregated['TAT (days)'].shape[0] > 1:  # Ensure at least 2 data points for histogram
            # Set the number of bins equal to the maximum value of 'TAT (days)'
            num_bins = int(aggregated['TAT (days)'].max())  # Number of bins is equal to max value of TAT (days)
            num_bins = max(num_bins, 1)  # Ensure that the number of bins is at least 1
            # Plot the histogram with normalized values (percentage)
            plt.figure(figsize=(10, 6))
            n, bins, patches = plt.hist(aggregated['TAT (days)'], bins=num_bins, edgecolor='black', density=True, color='#53A2BE')  # Normalize the histogram
            plt.title('Delivery Turnaround Time')
            plt.xlabel('Turnaround Time (days)')
            plt.ylabel('Percentage of Orders')  # Label updated to reflect percentage
            plt.grid(False)
            # Remove the top and right spines
            ax = plt.gca()  # Get the current axis
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            # Convert the y-axis ticks to percentages
            def percent(x, pos):
                return f'{100 * x:.1f}%'  # Format y-axis values as percentage            
            # Apply the percent formatter to y-axis ticks
            plt.gca().yaxis.set_major_formatter(FuncFormatter(percent))
            # Add percentages to each bar
            for patch in patches:
                height = patch.get_height()
                if height > 0:
                    percentage = height * 100  # Convert to percentage
                    plt.text(patch.get_x() + patch.get_width() / 2, height, f'{percentage:.1f}%', 
                            ha='center', va='bottom', fontsize=8, color='black')
            # Ensure x-axis ticks are integers
            plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
            # Step 5: Show the plot in Streamlit
            st.pyplot(plt, use_container_width=True)
        else:
            # Not enough data to create a histogram
            st.write("Not enough data to generate a histogram.")


multi_line_comment = ''' DATA PREVIEWS
st.subheader('Data Sample')
st.caption('Up to 3 random matching records')
if not filtered.empty:
    # Ensure the sample size is not larger than the number of rows in the DataFrame
    sample_size = min(3, len(filtered))  # Choose the smaller of 3 or the length of filtered
    st.write(filtered.sample(sample_size, replace=True))
else:
    st.write("No data matches these filters.")



st.subheader('Group by Order')
grouped_data = filtered.groupby('Order #').agg({
    'Customer': 'first',
    'Order Received': 'first',
    'Order Delivered': 'first',
    'Qty (Units)': 'sum',
    'Line Item Total ($)': 'sum',
    'Sales Rep': 'first',  # Get the first Sales Rep in each order group
})
grouped_data['Line Item Total ($)'] = grouped_data['Line Item Total ($)'].apply(lambda x: f"${x:,.2f}")
grouped_data = grouped_data.sort_values(by=['Order Received', 'Order Delivered'], ascending=False)

if not grouped_data.empty:
    st.write(grouped_data.head())
else:
    st.write('No data matches these filters.')
'''