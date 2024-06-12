let calorieCount = 0;
      

document.querySelector("form").addEventListener("submit", (e) => {
  e.preventDefault();

  const weight = parseFloat(document.getElementById("weight").value);
  const height = parseFloat(document.getElementById("height").value);
  const age = parseInt(document.getElementById("age").value);
  const genderElement = document.querySelector('input[name="gender"]:checked');
  const gender = genderElement ? genderElement.value : '';
  const activity = document.getElementById("activity").value;
 

  if (!weight ||!height ||!age ||!gender ||!activity) {
    alert("Please fill in all fields");
    return;
  }

  if (weight <= 0 || height <= 0 || age <= 0) {
    alert("Please enter valid values for weight, height, and age");
    return;
  }

  const calorieNeeds = calculateCalorieNeeds(weight, height, age, gender, activity);
  document.getElementById("calorie-count").innerText = `Your daily calorie needs are: ${calorieNeeds} calories`;
  
  
  window.location.href = "/profile/fgygdjfgygfuywgfwqy";
});

function calculateCalorieNeeds(weight, height, age, gender, activity) {
  let calorieNeeds = 0;
  if (gender === "male") {
    calorieNeeds = 66 + (6.2 * weight) + (12.7 * height) - (6.8 * age);
  } else {
    calorieNeeds = 655 + (4.35 * weight) + (4.7 * height) - (4.7 * age);
  }

  switch (activity) {
    case "sedentary":
      calorieNeeds *= 1.2;
      break;
    case "lightly active":
      calorieNeeds *= 1.375;
      break;
    case "moderately active":
      calorieNeeds *= 1.55;
      break;
    case "very active":
      calorieNeeds *= 1.725;
      break;
  }

  return Math.round(calorieNeeds);
}
