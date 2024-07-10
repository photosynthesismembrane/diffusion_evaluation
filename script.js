let currentIndex = 0;
const imagesPerPage = 1;
let selectedQuestions = [];
let image_folder = 'llava_composition_generations';
let image_data = llava_data;
// let questions = questions;

// Load the image data
// const image_data = {/* content from reformatted_image_data.js */};
// Assuming image_data.js is already included in the HTML

// Function to shuffle array elements
function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function truncateText(text, maxChars) {
    if (text.length <= maxChars) {
        return text;
    }
    let truncated = text.substring(0, maxChars);
    const lastSentenceEnd = Math.max(truncated.lastIndexOf('.'), truncated.lastIndexOf('!'), truncated.lastIndexOf('?'));
    if (lastSentenceEnd > -1) {
        truncated = truncated.substring(0, lastSentenceEnd + 1);
    } else {
        truncated = truncated.substring(0, truncated.lastIndexOf(' '));
    }
    return truncated.trim();
}

// Function to populate questions
function populateQuestions() {
    const questionsContainer = document.getElementById('questions-container');
    questionsContainer.innerHTML = ``;
    questions.forEach(questionObj => {
        const questionItem = document.createElement('div');
        questionItem.className = 'question-item';
        questionItem.innerText = questionObj.question;
        questionItem.onclick = () => handleQuestionClick(questionItem, questionObj.label);
        questionsContainer.appendChild(questionItem);
    });
}

// Handle question click
function handleQuestionClick(questionItem, questionLabel) {

    const previouslySelected = document.querySelector('.question-item.selected');
    if (previouslySelected) {
        previouslySelected.classList.remove('selected');
    }
    questionItem.classList.add('selected');
    selectedQuestions = [questionLabel];

    loadImages(currentIndex);
}

// document.getElementById('multiple-questions').addEventListener('change', function() {
//     if (!this.checked) {
//         const selectedItems = document.querySelectorAll('.question-item.selected');
//         selectedItems.forEach(item => item.classList.remove('selected'));
//         selectedQuestions = [];
//         loadImages(currentIndex);
//     }
// });

function changeDataSource() {
    const dataSource = document.getElementById('data-source').value;
    if (dataSource === 'pinterest') {
        image_folder = 'pinterest';
        image_data = pinterest_data;
    } else if (dataSource === 'renaissance') {
        image_folder = 'renaissance';
        image_data = renaissance_data;
    } else if (dataSource === 'band_poster') {
        image_folder = 'band_posters';
        image_data = band_poster_data;
    } else if (dataSource === 'landscape') {
        image_folder = 'landscape';
        image_data = landscape_data;
    } else if (dataSource === 'wikiart_selection') {
        image_folder = 'wikiart_selection';
        image_data = wikiart_selection_data;
    } else if (dataSource === 'graffiti') {
        image_folder = 'graffiti';
        image_data = grafitti_data;
    }
    populateQuestions();
    loadImages(currentIndex);
}


// Load images
function loadImages(startIndex) {
    let model = 'llava';
    if (document.getElementById('llava').checked) {
        model = 'llava';
        image_data = llava_data
    } else if (document.getElementById('cogvlm').checked) {
        model = 'cogvlm';
        image_data = cogvlm_data;
    } else if (document.getElementById('deepseek').checked) {
        model = 'deepseek';
        image_data = deepseek_data;
    }
    
    if (selectedQuestions.length === 0) {
        return;
    }
    image_folder = `${model}_${selectedQuestions[0]}_generations`;
    console.log(image_folder);

    const imageContainer = document.getElementById('image-container');
    imageContainer.innerHTML = ''; // Clear previous images

    const imagesArray = Object.entries(image_data).map(([key, value]) => ({
        image_filename: key,
        ...value
    })).filter(image => !noDataForImage(image)).slice(startIndex, startIndex + imagesPerPage);

    function imageModelAnswersEmpty(image, model) {
        if  (!`${model}_answers` in image) {
            return true;
        }

        // Check all selected questions whether there is at least one answer for the model
        return selectedQuestions.every(question => 
            !(image[`${model}_answers`] && question in image[`${model}_answers`] && image[`${model}_answers`][question])
        );
    }

    function noDataForImage(image) {
        const llavaChecked = document.getElementById('llava').checked;
        const cogvlmChecked = document.getElementById('cogvlm').checked;
        const deepseekChecked = document.getElementById('deepseek').checked;

        if ((llavaChecked && imageModelAnswersEmpty(image, 'llava')) && (cogvlmChecked && imageModelAnswersEmpty(image, 'cogvlm')) && (deepseekChecked && imageModelAnswersEmpty(image, 'deepseek'))) {
            return true;
        }
        return false;
    }

    // CHECK IF IMAGE EXISTS
    function checkIfImageExists(url, callback) {
        const img = new Image();
        img.src = url;
        
        if (img.complete) {
            callback(true);
        } else {
            img.onload = () => {
                callback(true);
            };
        
            img.onerror = () => {
                callback(false);
            };
        }
    }
  

    imagesArray.forEach((image, index) => {
        if (noDataForImage(image)) {
            return;
        }

        // Loop 20 times
        for (let i = 0; i < 10; i++) {
            const imageWrapper = document.createElement('div');
            imageWrapper.className = 'image-wrapper';

            const imgElement = document.createElement('img');
            imgElement.src = `${image_folder}/${model}_${selectedQuestions[0]}_${image.image_filename}_${i}.png`;
            // If image does not exist in the folder, skip
            if (model === 'cogvlm' || model === 'deepseek') {
                continue
            }

            if (! (selectedQuestions[0] === 'composition' || selectedQuestions[0] === 'focus_point' || selectedQuestions[0] === 'contrast_elements') ) {
                continue
            }
            
            imgElement.alt = `Image ${startIndex + index + 1}`;
            imageWrapper.appendChild(imgElement);

            const answersDiv = document.createElement('div');
            answersDiv.className = 'answers';

            const llavaChecked = document.getElementById('llava').checked;
            const cogvlmChecked = document.getElementById('cogvlm').checked;
            const deepseekChecked = document.getElementById('deepseek').checked;

            if (llavaChecked && !imageModelAnswersEmpty(image, 'llava')) {
                const llavaDiv = document.createElement('div');
                llavaDiv.className = 'answer-box';
                text =  truncateText(selectedQuestions.map(question => image.llava_answers[question] || "N/A").join('<br>'), 1000);
                llavaDiv.innerHTML += `<p><strong>llava:</strong><br>${text}</p>`;
                answersDiv.appendChild(llavaDiv);
            }
            if (cogvlmChecked && !imageModelAnswersEmpty(image, 'cogvlm')) {
                const cogvlmDiv = document.createElement('div');
                cogvlmDiv.className = 'answer-box';
                text = truncateText(selectedQuestions.map(question => image.cogvlm_answers[question] || "N/A").join('<br>'), 1000);
                cogvlmDiv.innerHTML += `<p><strong>cogvlm:</strong><br>${text}</p>`;
                answersDiv.appendChild(cogvlmDiv);
            }
            if (deepseekChecked && !imageModelAnswersEmpty(image, 'deepseek')) {
                const deepseekDiv = document.createElement('div');
                deepseekDiv.className = 'answer-box';
                text = truncateText(selectedQuestions.map(question => image.deepseek_answers[question] || "N/A").join('<br>'), 1000);
                deepseekDiv.innerHTML += `<p><strong>deepseek:</strong><br>${text}</p>`;
                answersDiv.appendChild(deepseekDiv);
            }

            imageWrapper.appendChild(answersDiv);
            imageContainer.appendChild(imageWrapper);
        }
    });
}

// Navigation functions
function loadPrevious() {
    if (currentIndex > 0) {
        currentIndex -= imagesPerPage;
        loadImages(currentIndex);
        scrollToFirstImage();
    }
}

function loadNext() {
    if (currentIndex + imagesPerPage < Object.keys(image_data).length) {
        currentIndex += imagesPerPage;
        loadImages(currentIndex);
        scrollToFirstImage();
    }
}

// Function to scroll to the first image
function scrollToFirstImage() {
    const firstImage = document.querySelector('#image-container img');
    if (firstImage) {
        firstImage.scrollIntoView({ behavior: 'smooth' });
    }
}


// Initialize
populateQuestions();
// document.getElementById('multiple-questions').addEventListener('change', function() {
//     if (!this.checked) {
//         const selectedItems = document.querySelectorAll('.question-item.selected');
//         selectedItems.forEach(item => item.classList.remove('selected'));
//         selectedQuestions = [];
//         loadImages(currentIndex);
//     }
// });

document.getElementById('llava').addEventListener('change', () => loadImages(currentIndex));
document.getElementById('cogvlm').addEventListener('change', () => loadImages(currentIndex));
document.getElementById('deepseek').addEventListener('change', () => loadImages(currentIndex));
// document.getElementById('data-source').addEventListener('change', changeDataSource);

loadImages(currentIndex);

