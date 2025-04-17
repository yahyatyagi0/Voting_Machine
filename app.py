import streamlit as st
import pandas as pd
import time

# Config
st.set_page_config(page_title="Voting Machine", layout="centered")

# CSS styling for background and playful UI
st.markdown("""
    <style>
        .main {
            background: linear-gradient(to bottom, #fff4f2, #ffdcdc);
            padding: 2rem;
            border-radius: 15px;
        }
        h1, h2 {
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
        .vote-btn {
            margin-top: 10px;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            margin-top: 3rem;
            color: #555;
        }
        .footer b:hover {
            color: #e63946;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🗳️ Fun Voting Machine</h1>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state variables
if "candidates" not in st.session_state:
    st.session_state.candidates = []
if "votes" not in st.session_state:
    st.session_state.votes = []
if "voting_started" not in st.session_state:
    st.session_state.voting_started = False
if "voted" not in st.session_state:
    st.session_state.voted = False
if "show_results" not in st.session_state:
    st.session_state.show_results = False

# Step 1: Add Candidates
if not st.session_state.voting_started:
    st.subheader("🎈 Add Candidates")
    n = st.number_input("How many candidates?", min_value=2, max_value=10, step=1)

    candidate_inputs = []
    for i in range(n):
        name = st.text_input(f"Candidate {i + 1}", key=f"cand_{i}")
        candidate_inputs.append(name)

    if st.button("🚀 Start Voting"):
        if all(name.strip() != "" for name in candidate_inputs):
            st.session_state.candidates = candidate_inputs
            st.session_state.votes = [0] * len(candidate_inputs)
            st.session_state.voting_started = True
            st.session_state.voted = False
            st.session_state.show_results = False
            st.rerun()
        else:
            st.warning("⚠️ Please enter all candidate names.")

# Step 2: Voting Section
elif st.session_state.voting_started and not st.session_state.voted:
    st.subheader("🗳️ Cast Your Vote")
    st.write("Click the vote button next to your chosen candidate.🤏🏼")

    for idx, candidate in enumerate(st.session_state.candidates):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### 👤 {candidate}")
        with col2:
            if st.button("✅ Vote", key=f"vote_button_{idx}_{candidate}"):
                st.session_state.votes[idx] += 1
                st.session_state.voted = True
                st.success("✅ Your vote has been recorded securely!")
                st.balloons()
                st.rerun()

# Step 3: Post-Vote Options
elif st.session_state.voted and not st.session_state.show_results:
    st.info("✅ Thank you! Your vote has been recorded.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📢 End Voting & Show Results"):
            st.session_state.show_results = True
            st.rerun()
    with col2:
        if st.button("🔁 Allow another voter"):
            st.session_state.voted = False
            st.rerun()

# Step 4: Results
elif st.session_state.show_results:
    st.subheader("📊 Voting Results")
    df = pd.DataFrame({
        "Candidate": st.session_state.candidates,
        "Votes": st.session_state.votes
    })

    st.bar_chart(df.set_index("Candidate"))

    max_votes = max(st.session_state.votes)
    winners = [st.session_state.candidates[i] for i, v in enumerate(st.session_state.votes) if v == max_votes]

    time.sleep(1)
    st.markdown("### 🏁 Final Result:")
    time.sleep(1)

    if len(winners) == 1:
        st.success(f"🏆 The winner is **{winners[0]}**! 🎉")
    else:
        st.warning("🤝 It's a tie between:")
        for w in winners:
            st.write(f"🥇 {w}")

    st.snow()

    if st.button("🔄 Restart Voting"):
        st.session_state.candidates = []
        st.session_state.votes = []
        st.session_state.voting_started = False
        st.session_state.voted = False
        st.session_state.show_results = False
        st.rerun()

# Footer credit
st.markdown("---")
st.markdown(
    """
    <div class="footer">
         Built with ❤️ by <b>Yahya Tyagi</b>
    </div>
    """,
    unsafe_allow_html=True
)