<?php
  $weight = isset($_POST['weight'])? $_POST['weight'] : null;
  $height = isset($_POST['height'])? $_POST['height'] : null;
  $age = isset($_POST['age'])? $_POST['age'] : null;
  $gender = isset($_POST['gender'])? $_POST['gender'] : null;
  $activity = isset($_POST['activity'])? $_POST['activity'] : null;

  if (!isset($weight, $height, $age, $gender, $activity)) {
    echo "Please fill in all the fields.";
    return;
  }

  if ($gender == 'female') {
    $bmr = 655 + (9.6 * $weight) + (1.8 * $height) - (4.7 * $age);
  } else {
    $bmr = 66 + (13.7 * $weight) + (5 * $height) - (6.8 * $age);
  }

  switch ($activity) {
    case 'sedentary':
      $tdee = $bmr * 1.2;
      break;
    case 'lightly active':
      $tdee = $bmr * 1.375;
      break;
    case 'moderately active':
      $tdee = $bmr * 1.55;
      break;
    case 'very active':
      $tdee = $bmr * 1.725;
      break;
  }

  echo "Your daily calories intake is: ". $tdee;
?>