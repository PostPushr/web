package com.postpushr;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;

public class SignInActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_signin);
		
		System.err.println("hello");
		
		getFragmentManager().beginTransaction().add(R.id.signin_fragment_container, new LoginFragment()).addToBackStack("Add RegisterFragment").commit();

	}

	/*@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.setup_actions, menu);
		return super.onCreateOptionsMenu(menu);
	}*/

}
