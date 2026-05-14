import streamlit as st
import sqlite3
import bcrypt


# =========================================
# REGISTER USER
# =========================================

def register_user(username, email, password):

    conn = sqlite3.connect("auth/database.db")

    cursor = conn.cursor()

    # HASH PASSWORD
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(
            """
            INSERT INTO users (
                username,
                email,
                password
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                hashed_password
            )
        )

        conn.commit()

        st.success(
            "✅ Account Created Successfully"
        )

    except sqlite3.IntegrityError:

        st.error(
            "⚠️ Email Already Exists"
        )

    except Exception as e:

        st.error(f"❌ Error: {e}")

    finally:

        conn.close()


# =========================================
# REGISTER PAGE
# =========================================

def register_page():

    st.title("📝 Create Account")

    st.markdown(
        "Create your InsightAI account"
    )

    username = st.text_input(
        "Username"
    )

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register"):

        # EMPTY CHECK
        if not username or not email or not password:

            st.warning(
                "⚠️ Please fill all fields"
            )

        # PASSWORD MATCH
        elif password != confirm_password:

            st.error(
                "❌ Passwords do not match"
            )

        # PASSWORD LENGTH
        elif len(password) < 6:

            st.warning(
                "⚠️ Password must be at least 6 characters"
            )

        else:

            register_user(
                username,
               email,
                password
            )


# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    register_page()