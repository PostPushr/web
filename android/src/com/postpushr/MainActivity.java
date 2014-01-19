package com.postpushr;

import android.app.Activity;
import android.os.Bundle;

import com.postpushr.fragments.HomeFragment;
import com.postpushr.fragments.LoginFragment;
import com.postpushr.fragments.RegisterFragment;
import com.postpushr.fragments.SignInFragment;
import com.postpushr.fragments.SignInFragment.SignInListener;
import com.postpushr.model.Account;

public class MainActivity extends Activity implements SignInListener {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		getFragmentManager().beginTransaction()
				.add(R.id.fragment_container, new SignInFragment()).commit();
	}

	@Override
	public void switchToLoginFragment() {
		getFragmentManager().beginTransaction()
				.replace(R.id.fragment_container, new LoginFragment())
				.addToBackStack("Replace with LoginFragment").commit();
	}

	@Override
	public void switchToRegisterFragment() {
		getFragmentManager().beginTransaction()
				.replace(R.id.fragment_container, new RegisterFragment())
				.addToBackStack("Replace with RegisterFragment").commit();
	}

	// TODO: implement validation in the original caller
	@Override
	public void moveToHomeFragment(Account account) {
		HomeFragment homeFragment = new HomeFragment();
		getFragmentManager().beginTransaction()
				.replace(R.id.fragment_container, homeFragment).commit();
		homeFragment.setListAdapter(homeFragment.new OrderListAdapter(this,
				account));

	}

	private String hashPassword(String password) {
		return Util.Sha1Hash(Util.Sha1Hash(password)
				+ Util.Sha1Hash(Secrets.getSalt()));
	}

	/*
	 * @Override public boolean onCreateOptionsMenu(Menu menu) { MenuInflater
	 * inflater = getMenuInflater(); inflater.inflate(R.menu.setup_actions,
	 * menu); return super.onCreateOptionsMenu(menu); }
	 */

}
