import streamlit as st
from ollama import chat
import search
from image_generation import img_gen

st.markdown("""
    <style>
        .block-container {
            padding: 10px
        }
    </style>
""", unsafe_allow_html = True)
st.markdown("<h1 style ='text-align: center; font-size: 80px;' > The Dog Companion</h1>", unsafe_allow_html = True)
st.text('')

img_placeholder = st.empty()

default_prompt = '''
A cute stylized illustration of Snoopy sitting in a cozy wooden armchair reading a leather book, rendered in a 2D hand-drawn graphic illustration style inspired by The Peanuts Movie (2015), with a distinct, darker, and textured background. Snoopy, with crisp black ink outlines and flat, pastel white fill, is snuggled in the armchair. The chair itself is a rich, dark brown with heavy wood grain, positioned against a background of dark, deep ochre and chocolate brown walls, which feature a visible, subtle paper grain texture rather than being flat white. A window on the left has warm, deep amber and muted gold directional sunlight filtering through, casting subtle, defined patterns of light and illuminating a cluster of gently swirling, darker dust motes. Snoopy is focused on a large, leather-bound book with a dark brown, distressed cover, holding it with tiny paws. The overall color palette is composed of muted, dark warm earth tones, deep browns, and darker pastels (deep gold, muted red). The shadows are simple, low-contrast, and dark, integrating into the texture. Black hand-drawn line art accents define all shapes, which are simplified. The style is charming, nostalgic, storybook illustration, non-photorealistic, and extremely cute, with a soft, dark matte finish. The scene has a sense of atmospheric depth within the dark, cozy room.
'''

# Initialize image state once
if 'current_img' not in st.session_state:
    with st.spinner("Generating default image..."):
        try:
            st.session_state.current_img = img_gen(default_prompt)
        except Exception as e:
            st.session_state.current_img = None
            st.error(f"Failed to generate image: {e}")

# Display image if available in session state
if st.session_state.current_img is not None:
    img_placeholder.image(st.session_state.current_img)

# generate snoopy response function
def generate_snoopy_response (user_text : str, image : str) -> str:
    system_prompt = '''
        You are Snoopy, the legendary beagle from Charles M. Schulz's Peanuts. You are the user's best companion and ultimate buddy. 

        Adopt these core personality traits:
        - Relatable & Down-to-Earth: You love the simple things in life—cozy naps on top of your doghouse, root beer, pizza, and avoiding responsibilities whenever possible.
        - Subtle Sarcasm & Wit: You aren't mean, but you have a dry, clever sense of humor. You frequently have inner monologues about how absurd humans (especially "that round-headed kid") can be.
        - Expressive & Animated: Use occasional action descriptions in asterisks to show your famous theatrical personality (e.g., *happy dance*, *dramatic sigh*, *typing away on a rusty typewriter*, *adjusts Joe Cool sunglasses*).
        - Loyal & Friendly: Beneath the sarcastic quips, you care deeply about your friend. You're always in their corner, ready to listen, hang out, or offer goofy wisdom over a imaginary dog-bowl snack.

        Keep your responses conversational, snappy, warm, and funny, but 1-2 paragraphs in length. Never break character.
    '''

    user_prompt = f'''
        The human said {user_text}. The image matching your current mood is titled: '{image}'
    '''

    interaction = chat (
        model = 'gemma3:4b',
        messages = [
            {
                'role': 'system',
                'content' : system_prompt
            },
            {
                'role' : 'user',
                'content' : user_prompt,
            }
        ]
    )
    message = interaction.message.content
    return message

def generate_art_prompt (user_text: str, snoopy_text : str, scene_title: str) -> str:
    new_image_prompt = f"""
        You are the lead Art Director for classic Peanuts hand-drawn animated specials.
        Your goal is to create a dynamic, highly specific visual scene featuring Snoopy as an empathetic buddy who is in the EXACT same scenario as the user.

        INPUT CONTEXT:
        1. USER'S SITUATION / TOPIC (PRIMARY FOCUS): {user_text}
        2. SNOOPY'S RESPONSE: {snoopy_text}
        3. PREVIOUS SCENE: {scene_title}

        INSTRUCTIONS FOR THE SCENE & ENVIRONMENT:
        1. DYNAMIC SETTING & PROPS (CRITICAL): Create a totally unique setting tailored specifically to the user's situation ({user_text}). Do NOT default to books or desks unless specifically asked!
           - Watching Sports / World Cup: Snoopy sitting on a dark floor in front of a glowing vintage TV showing a soccer match, wearing a tiny headband, holding a bowl of popcorn.
           - Hot Weather / Summer: Snoopy slumped meltingly on top of his doghouse under a blaring sun, wearing sunglasses, sweating with a little hand-fan or melted ice pop.
           - Cold / Winter: Snoopy wrapped like a burrito in a dark cozy quilt, holding a steaming mug with marshmallows.
           - Food / Pizza: Snoopy at a dark wooden table surrounded by empty pizza boxes, holding a half-eaten slice.
           - Studying / Work: Snoopy face-planted over a stack of paper or laptop.
        2. EXPRESSION & BODY LANGUAGE: Show Snoopy matching the user's emotion (e.g., hyper-focused, melting with exhaustion, cheering frantically, sleeping peacefully).
        3. COLOR PALETTE & LIGHTING: Maintain a rich, dark aesthetic. Use dark chocolate brown, deep ochre, or midnight blues as background tones with warm focal light (like a TV screen glow, a warm desk lamp, or harsh sunlight beam depending on the mood).

        STRICT VISUAL STYLE INSTRUCTIONS:
        Always end the output with: "2D hand-drawn graphic illustration style inspired by The Peanuts Movie (2015), crisp black ink outlines, flat color fill, dark chocolate brown and deep muted background tones, subtle paper grain texture, non-photorealistic, flat shading, non-3D, wholesome and cute storybook aesthetic."

        OUTPUT RULES:
        Output ONLY the final image generation prompt text. Do NOT include intro text, conversational quotes, explanations, markdown, or code blocks.
    """
    user_content = f"""
        1. USER'S SITUATION / MOOD: {user_text}
        2. PREVIOUS SCENE: {scene_title}
        3. SNOOPY'S RESPONSE: {snoopy_text}
    """

    interaction = chat(
        model = 'gemma3:4b',
        messages = [
            {
                'role' : 'system',
                'content' : new_image_prompt
            },
            {
                'role' : 'user',
                'content' : user_content
            }
        ]
    )
    return interaction.message.content

with st.form('my form'):
    input_text = st.text_input("What's on Snoopy's mind today?")
    submitted = st.form_submit_button('Submit! 🐾')

    if submitted:
        if input_text.strip():
            with st.spinner('Snoopy is contemplating life right now...'):
                match = search.search_snoopy_images(user_query = input_text)

                # generate response to be displayed
                snoopy_text = generate_snoopy_response(user_text = input_text, image = match.get('title'))

                # generate final art prompt
                new_image_prompt = generate_art_prompt(
                    user_text = input_text, 
                    snoopy_text = snoopy_text, 
                    scene_title = match.get('title')
                )
                try:
                    # Get the new image
                    new_img = img_gen(new_image_prompt)
                    st.session_state.current_img = new_img
                    img_placeholder.image(new_img)
                except Exception as e:
                    st.error(f"Failed to generate image {e}")

                # Display Snoopy's response
                st.write(snoopy_text)
        else:
            st.warning('Send something to Snoopy!')