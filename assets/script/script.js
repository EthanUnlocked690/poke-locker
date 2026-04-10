function linkPokemonAccount() {
    // 1. Redirect to Pokemon GO sign-in page (example URL)
    const signInUrl = "https://pokemon.com";
    
    // In a real scenario, you'd use OAuth. Here we simulate a click 
    // and immediately confirm for the purpose of the demo.
    window.open(signInUrl, '_blank');

    // 2. Change image to confirmed
    const imgElement = document.getElementById('pokeImg');
    imgElement.src = 'pokemon-confirmed.png';
    imgElement.alt = 'Confirmed';

    // 3. Show Popup Message
    const popup = document.getElementById('confirmationPopup');
    popup.classList.remove('hidden');

    // Hide popup after 3 seconds
    setTimeout(() => {
        popup.classList.add('hidden');
    }, 3000);
}
