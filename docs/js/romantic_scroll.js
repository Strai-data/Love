const PASSCODE = 'lightbulb';



const state = {

    ticking: false,

};



const SUPABASE_URL = 'https://jhsqmtmehvwwvnkfjtxm.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impoc3FtdG1laHZ3d3Zua2ZqdHhtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkyMDA1OTAsImV4cCI6MjA3NDc3NjU5MH0.GZ1Vq4Xo2AJ1ONXViTVaD4FzlMBIfPTiJQz0m1TRsAI';
const SUPABASE_RING_ENDPOINT = `${SUPABASE_URL}/rest/v1/ring`;



document.addEventListener('DOMContentLoaded', () => {

    const lockScreen = document.getElementById('lock-screen');

    const lockContent = lockScreen?.querySelector('.lock-content');

    const form = document.getElementById('unlock-form');

    const input = document.getElementById('unlock-key');

    const error = lockScreen?.querySelector('.lock-error');

    const story = document.getElementById('story');

    const panels = Array.from(document.querySelectorAll('.panel'));

    const gallerySection = document.querySelector('.gallery-panel');


    let isUnlocked = document.body?.dataset?.isUnlocked === 'true';

    if (!form || !input || !error || !story || !lockScreen) {

        return;

    }

    if (isUnlocked) {

        document.body.classList.remove('locked');

        document.body.classList.add('unlocked');

        story.setAttribute('aria-hidden', 'false');

        lockScreen.setAttribute('aria-hidden', 'true');

        lockScreen.setAttribute('hidden', '');

    } else {

        story.setAttribute('aria-hidden', 'true');

        lockScreen.removeAttribute('hidden');

        lockScreen.setAttribute('aria-hidden', 'false');

    }

    const observer = new IntersectionObserver(handleReveal, {

        threshold: 0.35,

    });



    panels.forEach((panel) => observer.observe(panel));



    const galleryControls = gallerySection ? initHorizontalGallery(gallerySection) : null;

    // Ring size form
    const ringSizeForm = document.getElementById('ring-size-form');

    const ringSizeInput = document.getElementById('ring-size-input');

    const ringSizeFeedback = document.querySelector('[data-ring-size-feedback]');


    const ringCard = document.querySelector('[data-ring-card]');

    const ringCardTitle = ringCard ? ringCard.querySelector('[data-ring-card-title]') : null;

    const ringCardLayers = ringCard ? Array.from(ringCard.querySelectorAll('[data-ring-layer]')) : [];

    const ringLayerButtons = ringCard ? Array.from(ringCard.querySelectorAll('[data-ring-layer-next]')) : [];



    if (ringCard && ringCardTitle && ringCardLayers.length) {
        const setRingLayer = (targetLayer) => {
            ringCardLayers.forEach((layer) => {
                const isActive = layer.dataset.ringLayer === targetLayer;
                layer.classList.toggle('ring-card-layer--active', isActive);
                layer.toggleAttribute('hidden', !isActive);
            });

            const activeLayer = ringCardLayers.find((layer) => layer.dataset.ringLayer === targetLayer);
            if (activeLayer?.dataset.ringLayerTitle) {
                ringCardTitle.textContent = activeLayer.dataset.ringLayerTitle;
            }

            if (targetLayer === 'form') {
                setRingSizeFeedback(ringSizeFeedback, '', '');
            }
        };

        const initialLayer = ringCardLayers.find((layer) => !layer.hasAttribute('hidden'));
        setRingLayer(initialLayer?.dataset.ringLayer || 'gift');

        ringLayerButtons.forEach((button) => {
            button.addEventListener('click', () => {
                const nextLayer = button.dataset.ringLayerNext;
                if (!nextLayer) {
                    return;
                }

                setRingLayer(nextLayer);

                if (nextLayer === 'message') {
                    const followUpButton = ringCard.querySelector('[data-ring-layer="message"] [data-ring-layer-next]');
                    followUpButton?.focus({ preventScroll: true });
                }

                if (nextLayer === 'form') {
                    ringSizeInput?.focus({ preventScroll: true });
                }
            });
        });
    }

    if (ringSizeForm && ringSizeInput && ringSizeFeedback) {
        const ringSizeSubmitButton = ringSizeForm.querySelector('[type="submit"]');
        const ringSizeStorageKey = 'loveStoryRingSizes';

        const backupRingSize = (ringSizeValue) => {
            try {
                const raw = localStorage.getItem(ringSizeStorageKey) || '[]';
                const parsed = JSON.parse(raw);
                const entries = Array.isArray(parsed) ? parsed : [];
                entries.push({ value: ringSizeValue, timestamp: new Date().toISOString() });
                localStorage.setItem(ringSizeStorageKey, JSON.stringify(entries));
            } catch (storageError) {
                return;
            }
        };

        // Submit ring size to Supabase
        const submitRingSizeToSupabase = async (ringSizeValue) => {
            const response = await fetch(`${SUPABASE_RING_ENDPOINT}?id=eq.1`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    apikey: SUPABASE_KEY,
                    Authorization: `Bearer ${SUPABASE_KEY}`,
                    Prefer: 'return=minimal',
                },
                body: JSON.stringify({ ring_size: ringSizeValue }),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Supabase update failed (${response.status}): ${errorText}`);
            }
        };

        ringSizeForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const value = ringSizeInput.value.trim();

            if (!value) {
                setRingSizeFeedback(ringSizeFeedback, 'Please add a size so I can take note.', 'error');
                ringSizeInput.focus({ preventScroll: true });
                return;
            }

            const defaultButtonLabel = ringSizeSubmitButton?.textContent;
            ringSizeSubmitButton?.setAttribute('disabled', 'true');
            if (ringSizeSubmitButton) {
                ringSizeSubmitButton.textContent = 'Sending...';
            }

            setRingSizeFeedback(ringSizeFeedback, 'Sending...', 'pending');

            try {
                await submitRingSizeToSupabase(value);

                backupRingSize(value);
                ringSizeForm.reset();
                setRingSizeFeedback(ringSizeFeedback, "Got it! I'll remember that.", 'success');
            } catch (submissionError) {
                console.error(submissionError);
                backupRingSize(value);
                setRingSizeFeedback(ringSizeFeedback, 'I could not send that just now, but I still love the thought.', 'error');
            } finally {
                if (ringSizeSubmitButton) {
                    ringSizeSubmitButton.removeAttribute('disabled');
                    if (defaultButtonLabel) {
                        ringSizeSubmitButton.textContent = defaultButtonLabel;
                    }
                }
            }
        });

        ringSizeInput.addEventListener('input', () => {
            if (ringSizeFeedback.textContent) {
                setRingSizeFeedback(ringSizeFeedback, '', '');
            }
        });
    }







    initImageLightbox('[data-lightbox]');









    form.addEventListener('submit', (event) => {



        event.preventDefault();



        if (isUnlocked) {



            return;



        }



        const value = input.value.trim().toLowerCase();



        if (!value) {



            showError(error, lockContent, 'Type the password to continue.');



            return;



        }



        if (value !== PASSCODE.toLowerCase()) {



            showError(error, lockContent, "That key doesn't fit quite yet. Try again.");



            input.select();



            return;



        }



        document.body.dataset.isUnlocked = 'true';



        isUnlocked = true;



        restartExperience({



            panels,



            galleryReset: (galleryControls ? galleryControls.reset : null),



        });



        unlockExperience(lockScreen, story);



        scheduleParallax(panels);



        input.value = '';



        error.textContent = '';



    });







    input.addEventListener('input', () => {



        error.textContent = '';



    });







    window.addEventListener('scroll', () => scheduleParallax(panels), { passive: true });



    window.addEventListener('resize', () => scheduleParallax(panels));



});







function restartExperience({ panels, galleryReset }) {

    window.scrollTo({ top: 0, behavior: 'auto' });



    panels.forEach((panel) => {

        panel.style.removeProperty('--parallax-offset');

    });



    if (typeof galleryReset === 'function') {

        galleryReset();

    }

}



function initHorizontalGallery(section) {

    const track = section.querySelector('[data-gallery-track]');

    const slides = Array.from(section.querySelectorAll('[data-gallery-slide]'));

    const prevButton = section.querySelector('[data-gallery-prev]');

    const nextButton = section.querySelector('[data-gallery-next]');



    if (!track || slides.length === 0) {

        return;

    }



    let activeIndex = 0;

    let slideSpan = 0;

    let scrollAccumulator = 0;

    let isActive = false;

    let isTouching = false;

    let touchStartX = 0;

    let touchStartY = 0;



    const updateActiveState = () => {

        slides.forEach((slide, index) => {

            const isCurrent = index === activeIndex;

            slide.classList.toggle('is-active', isCurrent);

            slide.setAttribute('aria-hidden', isCurrent ? 'false' : 'true');

        });



        if (prevButton) {

            prevButton.disabled = activeIndex === 0;

        }

        if (nextButton) {

            nextButton.disabled = activeIndex === slides.length - 1;

        }

    };



    const setTrackPosition = (animate = true) => {

        if (!slideSpan) {

            updateActiveState();

            return;

        }



        if (!animate) {

            track.style.transition = 'none';

        }



        track.style.transform = `translate3d(${-activeIndex * slideSpan}px, 0, 0)`;



        if (!animate) {

            void track.offsetWidth;

            track.style.transition = '';

        }



        updateActiveState();

    };



    const updateMeasurements = () => {

        if (!slides.length) {

            return;

        }



        const rect = slides[0].getBoundingClientRect();



        if (!rect.width) {

            window.requestAnimationFrame(updateMeasurements);

            return;

        }



        const trackStyles = window.getComputedStyle(track);

        const gapValue = parseFloat(trackStyles.getPropertyValue('column-gap') || trackStyles.getPropertyValue('gap') || '0') || 0;

        slideSpan = rect.width + gapValue;

        setTrackPosition(false);

    };



    const goToSlide = (targetIndex, options = {}) => {

        const nextIndex = clamp(targetIndex, 0, slides.length - 1);

        const force = Boolean(options.force);

        const animate = options.animate !== false;



        if (nextIndex === activeIndex && !force) {

            return;

        }



        activeIndex = nextIndex;

        scrollAccumulator = 0;

        setTrackPosition(animate);

    };



    const wheelHandler = (event) => {

        if (!isActive || !slides.length) {

            return;

        }



        const horizontalIntent = Math.abs(event.deltaX) > Math.abs(event.deltaY) && Math.abs(event.deltaX) > 6;

        if (!horizontalIntent) {

            scrollAccumulator = 0;

            return;

        }



        const direction = event.deltaX > 0 ? 1 : -1;

        const atBoundary = (direction === 1 && activeIndex === slides.length - 1) || (direction === -1 && activeIndex === 0);



        if (atBoundary) {

            scrollAccumulator = 0;

            return;

        }



        if (Math.sign(scrollAccumulator) !== direction) {

            scrollAccumulator = 0;

        }



        scrollAccumulator += event.deltaX;



        if (Math.abs(scrollAccumulator) >= 80) {

            event.preventDefault();

            goToSlide(activeIndex + direction);

        }

    };



    const touchStartHandler = (event) => {

        if (!isActive || event.touches.length !== 1) {

            return;

        }



        isTouching = true;

        scrollAccumulator = 0;

        touchStartX = event.touches[0].clientX;

        touchStartY = event.touches[0].clientY;

    };



    const touchMoveHandler = (event) => {

        if (!isActive || !isTouching || event.touches.length !== 1) {

            return;

        }



        const touch = event.touches[0];

        const deltaX = touchStartX - touch.clientX;

        const deltaY = touchStartY - touch.clientY;



        if (Math.abs(deltaY) > Math.abs(deltaX) && Math.abs(deltaY) > 10) {

            isTouching = false;

            return;

        }



        const direction = deltaX > 0 ? 1 : -1;

        const atBoundary = (direction === 1 && activeIndex === slides.length - 1) || (direction === -1 && activeIndex === 0);



        if (atBoundary) {

            isTouching = false;

            return;

        }



        if (Math.abs(deltaX) > 40) {

            event.preventDefault();

            goToSlide(activeIndex + direction);

            touchStartX = touch.clientX;

            touchStartY = touch.clientY;

        }

    };



    const touchEndHandler = () => {

        isTouching = false;

        scrollAccumulator = 0;

    };



    const focusObserver = new IntersectionObserver((entries) => {

        entries.forEach((entry) => {

            if (entry.target !== section) {

                return;

            }



            isActive = entry.isIntersecting;

            section.classList.toggle('gallery-active', isActive);

            if (!isActive) {

                scrollAccumulator = 0;

            }

        });

    }, {

        threshold: 0.68,

    });



    focusObserver.observe(section);



    updateActiveState();

    updateMeasurements();

    window.addEventListener('resize', updateMeasurements);

    window.addEventListener('load', updateMeasurements);



    if (prevButton) {

        prevButton.addEventListener('click', () => goToSlide(activeIndex - 1));

    }

    if (nextButton) {

        nextButton.addEventListener('click', () => goToSlide(activeIndex + 1));

    }



    slides.forEach((slide, index) => {

        slide.addEventListener('click', (event) => {

            if (index === activeIndex) {

                return;

            }



            event.preventDefault();

            goToSlide(index);

        });

    });



    section.addEventListener('wheel', wheelHandler, { passive: false });

    section.addEventListener('touchstart', touchStartHandler, { passive: true });

    section.addEventListener('touchmove', touchMoveHandler, { passive: false });

    section.addEventListener('touchend', touchEndHandler, { passive: true });

    section.addEventListener('touchcancel', touchEndHandler, { passive: true });



    return {

        reset: () => goToSlide(0, { animate: false, force: true }),

    };

}



function clamp(value, min, max) {

    return Math.min(Math.max(value, min), max);

}



function setRingSizeFeedback(element, message, state) {

    if (!element) return;



    element.textContent = message;



    if (state) {

        element.dataset.state = state;

    } else {

        delete element.dataset.state;

    }

}





function initImageLightbox(selector) {
    const triggers = Array.from(document.querySelectorAll(selector));
    if (!triggers.length) {
        return;
    }

    const overlay = document.createElement('div');
    overlay.className = 'lightbox';
    overlay.setAttribute('data-lightbox-overlay', '');
    overlay.setAttribute('aria-hidden', 'true');

    const content = document.createElement('div');
    content.className = 'lightbox__content';
    content.setAttribute('role', 'dialog');
    content.setAttribute('aria-modal', 'true');
    content.setAttribute('aria-label', 'Expanded photo');

    const lightboxImage = document.createElement('img');
    lightboxImage.className = 'lightbox__image';

    const caption = document.createElement('p');
    caption.className = 'lightbox__caption';
    caption.setAttribute('data-lightbox-caption', '');

    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'lightbox__close';
    closeButton.setAttribute('data-lightbox-close', '');
    closeButton.setAttribute('aria-label', 'Close image');
    closeButton.innerHTML = '<span aria-hidden="true">&times;</span>';

    content.append(lightboxImage, caption, closeButton);
    overlay.appendChild(content);
    document.body.appendChild(overlay);

    let activeTrigger = null;

    const closeLightbox = () => {
        overlay.classList.remove('is-active');
        overlay.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('lightbox-open');
        lightboxImage.removeAttribute('src');
        lightboxImage.alt = '';
        caption.textContent = '';
        if (activeTrigger) {
            activeTrigger.focus({ preventScroll: true });
            activeTrigger = null;
        }
    };

    const openLightbox = (trigger) => {
        activeTrigger = trigger;
        const source = trigger.dataset.lightboxSrc || trigger.getAttribute('src');
        if (!source) {
            return;
        }

        lightboxImage.src = source;
        lightboxImage.alt = trigger.alt || '';
        const description = trigger.getAttribute('data-lightbox-caption') || trigger.alt || '';
        caption.textContent = description;

        overlay.classList.add('is-active');
        overlay.setAttribute('aria-hidden', 'false');
        document.body.classList.add('lightbox-open');
        closeButton.focus({ preventScroll: true });
    };

    const handleKeydown = (event) => {
        if (event.key === 'Escape' && overlay.classList.contains('is-active')) {
            closeLightbox();
        }
    };

    document.addEventListener('keydown', handleKeydown);

    overlay.addEventListener('click', (event) => {
        if (event.target === overlay || event.target.closest('[data-lightbox-close]')) {
            closeLightbox();
        }
    });

    closeButton.addEventListener('click', closeLightbox);

    triggers.forEach((trigger) => {
        if (!trigger.hasAttribute('tabindex')) {
            trigger.setAttribute('tabindex', '0');
        }

        trigger.addEventListener('click', (event) => {
            event.preventDefault();
            openLightbox(trigger);
        });

        trigger.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                openLightbox(trigger);
            }
        });
    });

    return {
        open: openLightbox,
        close: closeLightbox,
    };
}

function unlockExperience(lockScreen, story) {

    document.body.classList.remove('locked');

    document.body.classList.add('unlocked');

    story.setAttribute('aria-hidden', 'false');



    window.requestAnimationFrame(() => {

        window.scrollTo({ top: 0, behavior: 'auto' });

    });



    setTimeout(() => {

        lockScreen.setAttribute('aria-hidden', 'true');

    }, 600);

}



function showError(errorElement, lockContent, message) {

    errorElement.textContent = message;

    if (!lockContent) return;



    lockContent.classList.remove('shake');

    void lockContent.offsetWidth; // restart animation

    lockContent.classList.add('shake');

}



function handleReveal(entries) {

    entries.forEach((entry) => {

        if (entry.isIntersecting) {

            entry.target.classList.add('visible');

        }

    });

}



function scheduleParallax(panels) {

    if (state.ticking) return;

    state.ticking = true;

    window.requestAnimationFrame(() => {

        applyParallax(panels);

        state.ticking = false;

    });

}



function applyParallax(panels) {

    const viewportCenter = window.innerHeight / 2;



    panels.forEach((panel) => {

        const speed = Number(panel.dataset.speed || 0);

        if (!speed) {

            panel.style.setProperty('--parallax-offset', '0px');

            return;

        }



        const rect = panel.getBoundingClientRect();

        const panelCenter = rect.top + rect.height / 2;

        const distanceFromCenter = panelCenter - viewportCenter;

        const offset = -distanceFromCenter * speed * 0.12;

        panel.style.setProperty('--parallax-offset', `${offset}px`);

    });

}





























