$(function(){

	var error_name;
	var error_password;
	var error_check_password;
	var error_email;
	var error_check;

	$('#user_name').blur(function() {
		check_user_name();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#email').blur(function() {
		check_email();
	});

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});

	function check_user_name(){
		var len = $('#user_name').val().length;
		if(len<5||len>20)
		{
			$('#user_name').next().html('请输入5-20个字符的用户名');
			$('#user_name').next().show();
			error_name = true;
		}
		else
		{
			$.get('/user/register_judge/?user_name='+$('#user_name').val(), function (data) {
			    if(data.count==1)
			    {
			        $('#user_name').next().text('用户名已存在').show();
			        error_name = true;
			    }
			    else
			    {
			        $('#user_name').next().hide();
			        error_name = false;
			    }
			});
		}
	}

	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').next().html('密码最少8位，最长20位')
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}		
	}

	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}		
		
	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#email').val()))
		{
			$.get('/user/register_judge/?user_email='+$('#email').val(), function (data) {
			    if(data.count==1)
			    {
			        $('#email').next().text('该邮箱已存在').show();
			        error_email = true;
			    }
			    else
			    {
			        $('#email').next().hide();
			        error_email = false;
			    }
			});
		}
		else
		{
			$('#email').next().text('你输入的邮箱格式不正确').show();
			error_email = true;
		}
	}

	$('form').submit(function() {
		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();

		if (error_name || error_password || error_check_password || error_email || error_check)
		{
			return false;
		}

	});

})