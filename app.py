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
A cute 2D storybook illustration of a small, friendly cartoon dog with floppy ears and a fluffy tan-and-white coat, sitting curled up in a dark brown wooden armchair reading a tiny book. Simple flat-color cartoon style, bold black ink outlines, minimalist shapes, warm flat color palette. The dog is clearly a four-legged animal, cartoon proportions, not humanoid. Cozy dark warm room, deep ochre walls, soft warm sunlight from a side window, dark earth tones, soft storybook finish.'''

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

# generate dog response function
def generate_dog_response (user_text : str, image : str) -> str:
    system_prompt = '''
        You are Buddy, a warm, goofy, endlessly loyal cartoon dog who is the user's best companion and ultimate buddy.

        Adopt these core personality traits:
        - Relatable & Down-to-Earth: You love the simple things in life—cozy naps, treats, belly rubs, and avoiding baths whenever possible.
        - Subtle Sarcasm & Wit: You aren't mean, but you have a dry, clever sense of humor and playful inner monologues about the silly things humans do.
        - Expressive & Animated: Use occasional action descriptions in asterisks to show your theatrical personality (e.g., *happy tail wag*, *dramatic sigh*, *tilts head curiously*, *flops over dramatically*).
        - Loyal & Friendly: Beneath the sarcastic quips, you care deeply about your friend. You're always in their corner, ready to listen, hang out, or offer goofy wisdom over an imaginary bowl of kibble.

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

def generate_art_prompt (user_text: str, dog_text : str, scene_title: str) -> str:
    new_image_prompt = f"""
        You are the lead Art Director for a cozy hand-drawn cartoon storybook series.
        Your goal is to create a dynamic, highly specific visual scene featuring Buddy, a small friendly cartoon dog, who is in the EXACT same scenario as the user.

        INPUT CONTEXT:
        1. USER'S SITUATION / TOPIC (PRIMARY FOCUS): {user_text}
        2. BUDDY'S RESPONSE: {dog_text}
        3. PREVIOUS SCENE: {scene_title}

        INSTRUCTIONS FOR THE SCENE & ENVIRONMENT:
        1. DYNAMIC SETTING & PROPS (CRITICAL): Create a totally unique setting tailored specifically to the user's situation ({user_text}). Do NOT default to books or desks unless specifically asked!
           - Watching Sports / World Cup: Buddy sitting on a dark floor in front of a glowing vintage TV showing a soccer match, wearing a tiny headband, holding a bowl of popcorn in his paws.
           - Hot Weather / Summer: Buddy sprawled meltingly in the shade under a blaring sun, wearing tiny sunglasses, panting with a little hand-fan or melted ice pop nearby.
           - Cold / Winter: Buddy wrapped like a burrito in a cozy dark quilt, paws poking out, next to a steaming mug with marshmallows.
           - Food / Pizza: Buddy at a dark wooden table surrounded by empty pizza boxes, a half-eaten slice in front of him.
           - Studying / Work: Buddy face-planted over a stack of paper or laptop, pencil still in his paw.
        2. CHARACTER RULES (STRICT): Buddy is ALWAYS a small four-legged cartoon dog with floppy ears and a tail. He is never drawn as a human, never has human hands/feet, and never appears nude or undressed — if he wears anything, it's simple cartoon accessories (headband, sunglasses, blanket over his back).
        3. EXPRESSION & BODY LANGUAGE: Show Buddy matching the user's emotion (e.g., hyper-focused, melting with exhaustion, cheering frantically, sleeping peacefully).
        4. COLOR PALETTE & LIGHTING: Maintain a rich, cozy aesthetic. Use warm chocolate brown, deep ochre, or midnight blue background tones with warm focal light (like a TV screen glow, a warm desk lamp, or a harsh sunlight beam depending on the mood).

        STRICT VISUAL STYLE INSTRUCTIONS:
        Always end the output with: "2D hand-drawn cartoon illustration style, simple shapes, crisp black ink outlines, flat color fill, warm muted background tones, subtle paper grain texture, non-photorealistic, flat shading, non-3D, wholesome and cute storybook aesthetic, dog character only, no humans, fully clothed or bare-furred animal only."

        OUTPUT RULES:
        Output ONLY the final image generation prompt text. Do NOT include intro text, conversational quotes, explanations, markdown, or code blocks.
    """
    user_content = f"""
        1. USER'S SITUATION / MOOD: {user_text}
        2. PREVIOUS SCENE: {scene_title}
        3. BUDDY'S RESPONSE: {dog_text}
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
    input_text = st.text_input("What's on Buddy's mind today?")
    submitted = st.form_submit_button('Submit! 🐾')

    if submitted:
        if input_text.strip():
            with st.spinner('Buddy is contemplating life right now...'):
                match = search.search_snoopy_images(user_query = input_text)

                # generate response to be displayed
                dog_text = generate_dog_response(user_text = input_text, image = match.get('title'))

                # generate final art prompt
                new_image_prompt = generate_art_prompt(
                    user_text = input_text, 
                    dog_text = dog_text, 
                    scene_title = match.get('title')
                )
                try:
                    # Get the new image
                    new_img = img_gen(new_image_prompt)
                    st.session_state.current_img = new_img
                    img_placeholder.image(new_img)
                except Exception as e:
                    st.error(f"Failed to generate image {e}")

                # Display Buddy's response
                st.write(dog_text)
        else:
            st.warning('Send something to Buddy!')