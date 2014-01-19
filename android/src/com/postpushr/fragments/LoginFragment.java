package com.postpushr.fragments;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;

import com.postpushr.R;
import com.postpushr.Util;
import com.postpushr.fragments.SignInFragment.SignInListener;
import com.postpushr.model.Account;

public class LoginFragment extends Fragment {

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		getActivity().setTitle("Login");
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup parent, Bundle savedInstanceState) {
		View view = inflater.inflate(R.layout.fragment_login, parent, false);
		Button loginSubmitButton = (Button) view.findViewById(R.id.login_submit_button);
		loginSubmitButton.setOnClickListener(new LoginSubmitListener());
		return view;
	}

	private class LoginSubmitListener implements OnClickListener {
		@Override
		public void onClick(View view) {

			final String username = ((EditText) getView().findViewById(R.id.login_email_edittext)).getText().toString();
			final String password = ((EditText) getView().findViewById(R.id.login_password_edittext)).getText().toString();
			final String hashedSaltedPassword = Util.hashAndSaltPassword(password);

			// TODO: validate the info with the server
			// Assuming success, and getting the list of orders
			((SignInListener) getActivity()).moveToHomeFragment(new Account(username, hashedSaltedPassword, null));
		}
	}
}
