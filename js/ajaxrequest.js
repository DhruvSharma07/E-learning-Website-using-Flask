$(document).ready(function () {
  // Email verification
  $("#stuemail").on("keypress blur", function () {
    var reg = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
    var stuemail = $("#stuemail").val();

    $.ajax({
      url: "Student/addstudent.php",
      type: "post",
      data: {
        checkemail: "checkmail",
        stuemail: stuemail
      },
      success: function (data) {
        console.log(data);
        if (data != 0) {
          $("#statusMsg2").html(
            '<small style="color:red;"> Email ID Already Registered ! </small>'
          );
          $("#signup").attr("disabled", true);
        } else if (data == 0 && reg.test(stuemail)) {
          $("#statusMsg2").html(
            '<small style="color:green;"> There you go ! </small>'
          );
          $("#signup").attr("disabled", false);
        } else if (!reg.test(stuemail)) {
          $("#statusMsg2").html(
            '<small style="color:red;"> Please Enter Valid Email e.g. example@mail.com </small>'
          );
          $("#signup").attr("disabled", false);
        }

        if (stuemail == "") {
          $("#statusMsg2").html(
            '<small style="color:red;"> Please Enter Email ! </small>'
          );
        }
      }
    });
  });
});

// Ajax call for adding new student
function addStu() {
  var reg = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
  var reg1 = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/i;
  var stuname = $("#stuname").val();
  var stuemail = $("#stuemail").val();
  var stupass = $("#stupass").val();
  // Checking fields on form submission
  if (stuname.trim() == "") {
    $("#statusMsg1").html(
      '<small style="color:red;"> Please Enter Name ! </small>'
    );
    $("#stuname").focus();
    return false;
  } else if (stuemail.trim() == "") {
    $("#statusMsg2").html(
      '<small style="color:red;"> Please Enter Email ! </small>'
    );
    $("#stuemail").focus();
    return false;
  } else if (stuemail.trim() != "" && !reg.test(stuemail)) {
    $("#statusMsg2").html(
      '<small style="color:red;"> Please Enter Valid Email e.g. example@mail.com </small>'
    );
    $("#stuemail").focus();
    return false;
  } else if (stupass.trim() == "") {
    $("#statusMsg3").html(
      '<small style="color:red;"> Please Enter Password ! </small>'
    );
    $("#stupass").focus();
    return false;
  } else if (stuemail.trim() != "" && !reg1.test(stupass)) {
    $("#statusMsg3").html(
      '<small style="color:red;"> Please Enter Valid Password e.g. Xyz@1234 </small>'
    );
    $("#stupass").focus();
    return false;
  } else {
    $.ajax({
      url: "Student/addstudent.php",
      type: "post",
      data: {
        stusignup: "stusignup",
        stuname: stuname,
        stuemail: stuemail,
        stupass: stupass
      },
      success: function (data) {
        console.log(data);
        if (data == "OK") {
          $("#successMsg").html(
            '<span class="alert alert-success"> Registered Successfully! </span>'
          );
          clearStuRegField();
        } else if (data == "Failed") {
          $("#successMsg").html(
            '<span class="alert alert-danger"> Unable to Register! </span>'
          );
        }
      }
    });
  }
}

// Empty all fields and status messages
function clearStuRegField() {
  $("#stuRegForm").trigger("reset");
  $("#statusMsg1").html(" ");
  $("#statusMsg2").html(" ");
  $("#statusMsg3").html(" ");
}

function clearAllStuReg() {
  $("#successMsg").html(" ");
  clearStuRegField();
}

// Ajax call for student login verification
function checkStuLogin() {
  var stuLogEmail = $("#stuLogEmail").val();
  var stuLogPass = $("#stuLogPass").val();
  $.ajax({
    url: "Student/addstudent.php",
    type: "post",
    data: {
      checkLogemail: "checklogmail",
      stuLogEmail: stuLogEmail,
      stuLogPass: stuLogPass
    },
    success: function (data) {
      console.log(data);
      if (data == 0) {
        $("#statusLogMsg").html(
          '<small class="alert alert-danger"> Invalid Email ID or Password ! </small>'
        );
      } else if (data == 1) {
        $("#statusLogMsg").html(
          '<div class="spinner-border text-success" role="status"></div>'
        );
        // Empty login fields
        clearStuLoginField();
        setTimeout(() => {
          window.location.href = "index.php";
        }, 1000);
      }
    }
  });
}

// Empty login fields
function clearStuLoginField() {
  $("#stuLoginForm").trigger("reset");
}

// Empty login fields and status messages
function clearStuLoginWithStatus() {
  $("#statusLogMsg").html(" ");
  clearStuLoginField();
}
