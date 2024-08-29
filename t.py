import streamlit as st

# Define a Streamlit function to display and update the counter
def display_counter():
    # Check if the counter is in the cache
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    # Create a button to increment the counter
    if st.button("Increment Counter"):
        st.session_state.counter += 1

    # Display the current counter value
    st.write("Counter:", st.session_state.counter)

# Use the display_counter function in your Streamlit app
def main():
    st.title("Counter App")
    display_counter()

if __name__ == "__main__":
    main()