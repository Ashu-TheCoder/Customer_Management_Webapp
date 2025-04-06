    if submitted:
        if new_id and new_name and new_role:
            new_row = {"ID": int(new_id), "Name": new_name, "Role": new_role, "Gender": new_gender, "Status": new_status}
            st.session_state.data = st.session_state.data.append(new_row, ignore_index=True)
            st.success("New entry added!")

# Delete a Row
st.subheader("Delete Entry")
row_to_delete = st.number_input("Enter Row Index to Delete", min_value=0, max_value=len(st.session_state.data) - 1, step=1)
if st.button("Delete Entry"):
    st.session_state.data = st.session_state.data.drop(index=row_to_delete).reset_index(drop=True)
    st.success(f"Row {row_to_delete} deleted!")

# Update an Existing Row
st.subheader("Update Entry")
row_to_update = st.number_input("Enter Row Index to Update", min_value=0, max_value=len(st.session_state.data) - 1, step=1)
updated_name = st.text_input("Updated Name")
if st.button("Update Entry"):
    if updated_name:
        st.session_state.data.at[row_to_update, "Name"] = updated_name
        st.success(f"Row {row_to_update} updated!")

# Display updated table dynamically
st.write("Updated Table:")