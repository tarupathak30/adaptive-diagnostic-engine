let sessionId = null
let currentQuestion = null
let abilityHistory = [0.5]
let questionCount = 0

let chart = new Chart(document.getElementById("abilityChart"), {
    type: "line",
    data: {
        labels: [0],
        datasets: [{
            label: "Ability",
            data: abilityHistory
        }]
    }
})


// start the session ---> endpoint is POST/start-session 

async function startSession(){

    const res = await fetch("http://localhost:8000/start-session?user_id=test", 
        {
            method : "POST"
        }   
    )

    const data = await res.json()

    sessionId = data.session_id
    showQuestion(data.question)
}


// show the question 
function showQuestion(q){

    currentQuestion = q

    let html = `<h3>${q.question}</h3>`

    q.options.forEach(opt => {
        html += `
        <label>
        <input type="radio" name="answer" value="${opt}">
        ${opt}
        </label><br>`
    })

    document.getElementById("questionBox").innerHTML = html
}


// submit answer 
// endpoint - POST/submit-answer 

async function submitAnswer(){

    const selected =
        document.querySelector('input[name="answer"]:checked')?.value

    if(!selected){
        alert("Please select an answer")
        return
    }

    const res = await fetch("http://localhost:8000/submit-answer",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            session_id: sessionId,
            question_id: currentQuestion.id,
            selected_answer: selected
        })
    })

    const data = await res.json()

    // update ability graph
    abilityHistory.push(data.new_ability)

    chart.data.labels.push(abilityHistory.length)
    chart.data.datasets[0].data = abilityHistory
    chart.update()

    // update progress counter
    questionCount++

    document.getElementById("progress").innerText =
        `Questions answered: ${questionCount}/10`

    // show next question
    if(data.next_question){
        showQuestion(data.next_question)
    }
    else{
        document.getElementById("questionBox").innerHTML =
            "<h3>Test complete</h3>"
    }
}


// generate study plan 
async function generatePlan(){

    const res = await fetch(
        `http://localhost:8000/generate-study-plan/${sessionId}`
    )

    const data = await res.json()

    if(!res.ok){
        document.getElementById("studyPlan").innerText = data.detail
        return
    }

    document.getElementById("studyPlan").innerText = data.study_plan
}