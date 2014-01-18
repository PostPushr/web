package com.postpushr;

import com.postpushr.SignInFragment.SignInListener;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;

public class SignInActivity extends Activity implements SignInListener {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_signin);		
		getFragmentManager().beginTransaction().add(R.id.signin_fragment_container, new SignInFragment()).commit();

	}

	@Override
	public void onLoginButton() {
		getFragmentManager().beginTransaction().replace(R.id.signin_fragment_container, new LoginFragment()).addToBackStack("Replace with LoginFragment").commit();
	}

	@Override
	public void onRegisterButton() {
		getFragmentManager().beginTransaction().replace(R.id.signin_fragment_container, new RegisterFragment()).addToBackStack("Replace with RegisterFragment").commit();
	}

	
	
	
	/*@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.setup_actions, menu);
		return super.onCreateOptionsMenu(menu);
	}*/

}
